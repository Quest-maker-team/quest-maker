import {BlockRedactor} from './blockRedactor';
import {consume} from '@jsplumb/browser-ui';
import {Quest} from "./quest";

export class Render {
    static createEndpoint(instance, elem, anchors, options) {
        const endpoint = instance.addEndpoint(elem, anchors, options);
        elem.dispatchEvent(new CustomEvent('newEndpointCreating', {
            bubbles: true,
            detail: {
                endpointElem: endpoint.endpoint.canvas,
            },
        }));
    }

    static renderBlockBase(question, width, title, instance, sourceEndpoint) {
        const block = document.createElement('div');
        block.id = question.question_id;
        block.className = 'position-absolute card border-2 panzoom-exclude';
        block.style.width = width.toString();
        block.style.left = question.pos_x.toString() + 'px';
        block.style.top = question.pos_y.toString() + 'px';
        const blockBody = document.createElement('div');
        blockBody.className = 'card-body';
        blockBody.innerHTML = '<h5 class="card-title text-center">' + title + '</h5>' +
                                '<hr>' +
                                '<p class="card-text text-center text-truncate">' + question.text + '</p>';
        block.append(blockBody);

        block.ondblclick = () => {
            BlockRedactor.showRedactor(question, instance, sourceEndpoint);
        };

        document.getElementById('container').append(block);
        return block;
    }

    static deleteElemEndpoint(elem, instance) {
        instance.selectEndpoints({element: elem}).deleteAll();
        delete instance.getManagedElements()[elem.id];
    }

    static addDeleteButton(quest, block, instance, answerElements) {
        const deleteButton = document.createElement('button');
        deleteButton.id = 'btn' + block.id;
        deleteButton.className = 'btn-close btn-danger';
        deleteButton.style.position = 'absolute';
        deleteButton.style.top = '0';
        deleteButton.style.right = '0';
        deleteButton.onclick = () => {
            if (answerElements !== undefined) {
                for (const answerElement of answerElements) {
                    Render.deleteElemEndpoint(answerElement, instance);
                }
            }

            instance.selectEndpoints({element: block}).deleteAll();
            delete instance.getManagedElements()[block.id];
            block.parentElement.removeChild(block);
            const questions = quest.data.questions;
            questions.splice(questions.findIndex((question) => question.question_id == block.id), 1);
            Quest.deleteEntity('question', block.id);
        };
        block.append(deleteButton);
    }

    static renderStart(question, instance, sourceEndpoint) {
        const block = this.renderBlockBase(question, '10rem', 'Начало');

        const answer = document.createElement('div');
        answer.id = 'answer_option' + question.answer_options[0].answer_option_id;
        block.append(answer);

        instance.manage(block);
        Render.createEndpoint(instance, answer, {}, sourceEndpoint);
        return block;
    }

    static renderFinish(question, instance, targetEndpoint) {
        const block = this.renderBlockBase(question, '10rem', 'Конец');
        Render.createEndpoint(instance, block, {}, targetEndpoint);
        return block;
    }

    static updateAnswersEndpoints(question, instance) {
        const answerTable = document.getElementById('anstab' + question.question_id);
        for (const ans of answerTable.childNodes) {
            instance.revalidate(ans);
        }
    }

    static renderAnswer(answer, question, instance, sourceEndpoint, special) {
        const ansTable = document.getElementById('anstab' + question.question_id);
        const tableElement = document.createElement('li');
        tableElement.className = 'list-group-item';
        tableElement.id = 'answer_option' + answer.answer_option_id;

        if (special === true && answer.text === '') {
            tableElement.innerText = '<Неверный ответ>';
            ansTable.append(tableElement);
        } else {
            tableElement.innerText = answer.text;
            let last = ansTable.lastElementChild;
            if (last === null) {
                ansTable.append(tableElement);
            } else if (last.innerText === '<Неверный ответ>') {
                if (answer.text === 'skip') {
                    last.before(tableElement);
                } else {
                    last = last.previousElementSibling;
                    if (last === null) {
                        ansTable.prepend(tableElement);
                    } else if (last.innerText === 'skip') {
                        last.before(tableElement);
                    } else {
                        last.after(tableElement);
                    }
                }
            } else if (last.innerText === 'skip') {
                last.before(tableElement);
            } else {
                last.after(tableElement);
            }
        }
        Render.createEndpoint(instance, tableElement, {anchor: ['Right', 'Left']}, sourceEndpoint);
        for (const ans of ansTable.childNodes) {
            instance.revalidate(ans);
        }
    }

    static renderQuestion(quest, question, title, instance, sourceEndpoint, targetEndpoint) {
        const block = Render.renderBlockBase(question, '15rem', title, instance, sourceEndpoint);
        const answerTable = document.createElement('ul');
        answerTable.className = 'list-group list-group-flush';
        answerTable.id = 'anstab' + question.question_id;
        block.append(answerTable);
        for (const answer of question.answer_options) {
            Render.renderAnswer(answer, question, instance, sourceEndpoint, true);
        }

        Render.addDeleteButton(quest, block, instance, answerTable.childNodes);

        Render.createEndpoint(instance, block, {anchor: 'Top'}, targetEndpoint);

        return block;
    }

    static renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint) {
        const block = Render.renderBlockBase(question, '15rem', 'Перемещение', instance, sourceEndpoint);

        Render.addDeleteButton(quest, block, instance);

        const answer = document.createElement('div');
        answer.id = 'movement' + question.movements[0].movement_id;
        block.append(answer);

        Render.createEndpoint(instance, block, {anchor: 'Top'}, targetEndpoint);
        Render.createEndpoint(instance, answer, {anchor: 'Bottom'}, sourceEndpoint);

        return block;
    }

    static render(quest, instance, sourceEndpoint, targetEndpoint, panzoom) {
        for (const question of quest.data.questions) {
            let block;
            switch (question.type) {
            case 'start':
                block = Render.renderStart(question, instance, sourceEndpoint);
                break;
            case 'end':
                block = Render.renderFinish(question, instance, targetEndpoint);
                break;
            case 'open':
                block = Render.renderQuestion(quest, question,"Открытый вопрос", instance, sourceEndpoint, targetEndpoint);
                break;
            case 'movement':
                block = Render.renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint);
                break;
            case 'choice':
                block = Render.renderQuestion(quest, question, "Вопрос с выбором ответа", instance, sourceEndpoint, targetEndpoint);
                break;
            default:
                break;
            }
        }
        // Connect
        for (const question of quest.data.questions) {
            if (question.type === 'movement') {
                instance.connect({
                    source: instance.selectEndpoints({
                        element: document.getElementById('movement' + question.movements[0].movement_id),
                    }).get(0),
                    target: instance.selectEndpoints({
                        element: document.getElementById(question.movements[0].next_question_id)}).get(0),
                });
            } else if (question.type !== 'end') {
                for (const answer of question.answer_options) {
                    if (answer.next_question_id != null) {
                        instance.connect({
                            source: instance.selectEndpoints({
                                element: document.getElementById('answer_option' + answer.answer_option_id),
                            }).get(0),
                            target: instance.selectEndpoints({
                                element: document.getElementById(answer.next_question_id),
                            }).get(0),
                        });
                    }
                }
            }
        }
    }
}
