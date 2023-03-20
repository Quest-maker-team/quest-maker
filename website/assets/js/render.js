import {BlockRedactor} from './blockRedactor';
import {consume} from '@jsplumb/browser-ui';
import {Quest} from './quest';

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

    static renderBlockBase(questBlock, width, title, instance, sourceEndpoint, quest) {
        const block = document.createElement('div');
        block.id = questBlock.block_id;
        block.className = 'position-absolute card border-2 panzoom-exclude';
        block.style.width = width.toString();
        block.style.left = questBlock.pos_x.toString() + 'px';
        block.style.top = questBlock.pos_y.toString() + 'px';

        const blockBody = document.createElement('div');
        blockBody.className = 'card-body';
        blockBody.id = 'body' + questBlock.block_id;
        blockBody.innerHTML = '<h5 class="card-title text-center">' + title + '</h5>' +
                                '<hr>' +
                                '<p class="card-text text-center text-truncate">' + questBlock.block_text + '</p>';
        block.append(blockBody);

        const redactButton = document.createElement('button');
        redactButton.insertAdjacentHTML('beforeend',
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"' +
                    'fill="currentColor"' +
                    'className="bi bi-pen" viewBox="0 0 16 16">' +
                '<path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0' +
                        '1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5' +
                        '4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0' +
                        '1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821' +
                        '3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0' +
                        '1-.468-.325z"/>' +
            '</svg>');
        redactButton.id = 'btn' + block.id;
        redactButton.className = 'btn btn-outline-info py-0 px-1 border-0';
        redactButton.style.position = 'absolute';
        redactButton.style.zIndex = '100';
        redactButton.style.top = '0';
        redactButton.style.left = '0';
        redactButton.onclick = () => {
            BlockRedactor.showRedactor(questBlock, instance, sourceEndpoint, quest);
        };
        block.append(redactButton);

        block.ondblclick = () => {
            BlockRedactor.showRedactor(questBlock, instance, sourceEndpoint, quest);
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
        deleteButton.className = 'btn btn-outline-danger py-0 px-1 border-0';
        deleteButton.style.position = 'absolute';
        deleteButton.style.top = '0';
        deleteButton.style.right = '0';
        deleteButton.insertAdjacentHTML('beforeend',
                '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"' +
                        'class="bi bi-trash" viewBox="0 0 16 16">' +
                    '<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 ' +
                            '.5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 ' +
                            '0V6z"/>' +
                    '<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 ' +
                            '1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 ' +
                            '0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 ' +
                            '4H4.118zM2.5 3V2h11v1h-11z"/>' +
                '</svg>')
        deleteButton.onclick = () => {
            if (answerElements !== undefined) {
                for (const answerElement of answerElements) {
                    Render.deleteElemEndpoint(answerElement, instance);
                }
            }

            instance.selectEndpoints({element: document.getElementById('body' + block.id)}).deleteAll();
            delete instance.getManagedElements()[block.id];
            block.parentElement.removeChild(block);
            const questBlocks = quest.data.blocks;
            questBlocks.splice(questBlocks.findIndex((questBlock) => questBlock.block_id == block.id), 1);
            Quest.deleteEntity('block', block.id);
        };
        block.append(deleteButton);
    }

    static renderStart(questBlock, instance, sourceEndpoint) {
        console.log("render start");
        const block = this.renderBlockBase(questBlock, '10rem', 'Начало');
        block.className += ' text-white bg-success';
        /*const answer = document.createElement('div');
        answer.id = 'answer_option' + questBlock.answer_options[0].answer_option_id;
        answer.style.height = '100%';
        answer.style.width = '100%';
        answer.className = 'position-absolute';
        block.append(answer);*/

        instance.manage(block);
        Render.createEndpoint(instance, block, {anchor: ['Top', 'Right', 'Left', 'Bottom']}, sourceEndpoint);
        return block;
    }

    static renderFinish(quest, questBlock, instance, targetEndpoint) {
        console.log("render finish");
        const block = this.renderBlockBase(questBlock, '10rem', 'Конец');
        block.className += ' text-white bg-dark';
        instance.manage(block);
        Render.createEndpoint(instance, document.getElementById('body' + questBlock.block_id),
            {anchor: ['Top', 'Right', 'Left', 'Bottom']}, targetEndpoint);
        Render.addDeleteButton(quest, block, instance);
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
        tableElement.className = 'list-group-item text-truncate';
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
        if (question.type==='choice') {
            block.className+=' border-info';
        } else {
            block.className+=' border-primary';
        }
        const answerTable = document.createElement('ul');
        answerTable.className = 'list-group list-group-flush';
        answerTable.id = 'anstab' + question.question_id;
        block.append(answerTable);
        for (const answer of question.answer_options) {
            Render.renderAnswer(answer, question, instance, sourceEndpoint, true);
        }

        instance.manage(block);
        Render.addDeleteButton(quest, block, instance, answerTable.childNodes);
        Render.createEndpoint(instance, document.getElementById('body' + question.question_id),
            {anchor: ['Top', 'Right', 'Left']}, targetEndpoint);

        return block;
    }

    static renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint) {
        const block = Render.renderBlockBase(question, '15rem', 'Перемещение', instance, sourceEndpoint, quest);
        block.className+=' border-warning';
        const answer = document.createElement('div');
        answer.id = 'movement' + question.movements[0].movement_id;
        answer.style.height = '100%';
        answer.style.width = '100%';
        answer.className = 'position-absolute';
        block.append(answer);

        instance.manage(block);
        Render.addDeleteButton(quest, block, instance,
            [document.getElementById('movement' + question.movements[0].movement_id)]);
        Render.createEndpoint(instance, document.getElementById('body' + question.question_id),
            {anchor: ['Top', 'Right', 'Left', 'Bottom']}, targetEndpoint);
        Render.createEndpoint(instance, answer, {anchor: ['Bottom', 'Right', 'Left', 'Top']}, sourceEndpoint);

        return block;
    }

    static render(quest, instance, sourceEndpoint, targetEndpoint, panzoom) {
        for (const questBlock of quest.data.blocks) {
            let block;
            switch (questBlock.block_type_name) {
            case 'start_block':
                block = Render.renderStart(questBlock, instance, sourceEndpoint);
                break;
            case 'end_block':
                block = Render.renderFinish(quest, questBlock, instance, targetEndpoint);
                break;
            case 'open_question':
                block = Render.renderQuestion(quest, questBlock, 'Открытый вопрос', instance, sourceEndpoint,
                    targetEndpoint);
                break;
            case 'movement':
                block = Render.renderMovement(quest, questBlock, instance, sourceEndpoint, targetEndpoint);
                break;
            case 'choice_question':
                block = Render.renderQuestion(quest, questBlock, 'Вопрос с выбором ответа', instance, sourceEndpoint,
                    targetEndpoint);
                break;
            default:
                break;
            }
        }
        // Connect
        for (const questBlock of quest.data.blocks) {
            /*if (questBlock.type === 'movement') {
                instance.connect({
                    source: instance.selectEndpoints({
                        element: document.getElementById('movement' + questBlock.movements[0].movement_id),
                    }).get(0),
                    target: instance.selectEndpoints({
                        element: document.getElementById('body' + questBlock.movements[0].next_question_id)}).get(0),
                });
            } else if (questBlock.type !== 'end') {
                for (const answer of questBlock.answer_options) {
                    if (answer.next_question_id != null) {
                        instance.connect({
                            source: instance.selectEndpoints({
                                element: document.getElementById('answer_option' + answer.answer_option_id),
                            }).get(0),
                            target: instance.selectEndpoints({
                                element: document.getElementById('body' + answer.next_question_id),
                            }).get(0),
                        });
                    }
                }
            }*/
            if (questBlock.block_type_name == 'start_block') {
                console.log(instance.selectEndpoints({element: document.getElementById(questBlock.block_id),}).get(0),);
                console.log(instance.selectEndpoints({element: document.getElementById('body' + questBlock.next_question_id),}).get(0),);
                instance.connect({
                    source: instance.selectEndpoints({
                        element: document.getElementById(questBlock.block_id),
                    }).get(0),
                    target: instance.selectEndpoints({
                        element: document.getElementById('body' + questBlock.next_block_id),
                    }).get(0),
                });
                console.log("connect");
            }
        }
    }
}
