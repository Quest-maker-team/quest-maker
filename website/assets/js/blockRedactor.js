import {Quest} from './quest';
import * as bootstrap from 'bootstrap';
import { Render } from './render';

export class BlockRedactor {
    static addTextRedactor(form, label, text) {
        form.innerHTML +=
            '<label for="formControlTextarea" class="form-label">' + label + '</label>' +
            '<textarea class="form-control" id="formControlTextarea" rows="3">' +
            text +
            '</textarea>';
    }

    static deleteAnswer(answer, question, instance, withConfirm) {
        let conf = true;
        if (withConfirm)
            conf = confirm('Вы действительно хотите удалить вариант ответа? Отменить действие будет не возможно.');
        if (conf) {
            let index = 0;
            for (const ans of question.answer_options){
                if (ans.answer_option_id === answer.answer_option_id)
                    break;
                index += 1;
            }
            document.getElementById('ansblock' + answer.answer_option_id).remove();
            question.answer_options.splice(index, 1);
            let ans = document.getElementById('answer_option' + answer.answer_option_id);
            instance.deleteConnectionsForElement(ans);
            instance.selectEndpoints({element: ans}).deleteAll();
            delete instance.getManagedElements()[ans.id];
            ans.remove();
            Quest.deleteAnswer(answer.answer_option_id);
            let answerTable = document.getElementById('anstab' + question.question_id);
            for (const ans of answerTable.childNodes) {
                instance.revalidate(ans);
            }
        }
    }

    static addAnswerForQuestion(element_id, answer, question, instance) {
        document.getElementById(element_id).insertAdjacentHTML('beforeend',
            '<div class="row pb-1" id="ansblock' + answer.answer_option_id + '">' +
                '<div class="col-8">'+
                    '<input type="text" onkeydown="return (event.keyCode!=13);" class="form-control" id="answerText' +
                        answer.answer_option_id + '" value="' + answer.text + '" placeholder="Вариант ответа">' +
                    '<div class="invalid-feedback">' +
                        'Не используйте "skip" или пустую строку в качестве ответов. ' +
                        'Добавить возможность пропуска можно, установив соответствующий флаг.' +
                    '</div>' +
                '</div>' +
                '<div class="col-3">' +
                    '<div class="input-group">' +
                        '<span class="input-group-text"> Очки </span>' +
                        '<input type="number" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                            'id="answerPoints' + answer.answer_option_id + '" value="' + answer.points + '">' +
                    '</div>' +
                '</div>' +
                '<div class="col-1">' +
                    '<button type="button" class="btn btn-danger" id="ansdel' + answer.answer_option_id + '">' +
                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" ' +
                                'class="bi bi-trash" viewBox="0 0 16 16">' +
                            '<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 ' +
                                '.5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 ' +
                                '0V6z"/>' +
                            '<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 ' +
                                '1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 ' +
                                '0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 ' +
                                '4H4.118zM2.5 3V2h11v1h-11z"/>' +
                        '</svg>' +
                    '</button>' +
                '</div>' +
            '</div>'
        );
        document.getElementById('ansdel' + answer.answer_option_id).onclick = () => {
            this.deleteAnswer(answer, question, instance, true);
        }
    }

    static showSpecial(element_id, special, name, text) {
        document.getElementById(element_id).insertAdjacentHTML('afterend',
            '<div class="row pb-1" id="' + name + special.answer_option_id + '">' +
                '<div class="col-8">'+
                    '<input type="text" name="' + name + '" id="' + special.answer_option_id +
                        '" class="form-control" placeholder="' + text + '" readonly>' +
                '</div>' +
                '<div class="col-3">' +
                    '<div class="input-group">' +
                        '<span class="input-group-text"> Очки </span>' +
                        '<input type="number" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                            'id="answerPoints' + special.answer_option_id + '" value="' + special.points + '">' +
                    '</div>' +
                '</div>' +
            '</div>'
        );
    }

    static addSpecial(element_id, name, text, points, question, instance, sourceEndpoint){
        if (document.getElementsByName(name)[0] !== undefined) {
            return;
        }
        let answer;
        Quest.addAnswer(JSON.stringify({
            points: points,
            text: text,
        })).then((response) => {
            answer = {
                answer_option_id: JSON.parse(response).answer_option_id,
                points: points,
                text: text,
            };
            question.answer_options.push(answer);
            Render.renderAnswer(answer, question, instance, sourceEndpoint, true);
            if (text === '')
                text = '<Любой другой ответ>';
            this.showSpecial(element_id, answer, name, text);
        });
    }

    static deleteSpecial(name, question, instance) {
        let elem = document.getElementsByName(name)[0];
        if (elem === undefined) {
            return;
        }
        let id = elem.id;
        let index = 0;
        for (const ans of question.answer_options) {
            if (ans.answer_option_id == id) {
                break;
            }
            index += 1;
        }
        let box = document.getElementById(name + id);
        box.remove();
        question.answer_options.splice(index, 1);
        let ans = document.getElementById('answer_option' + id);
        instance.deleteConnectionsForElement(ans);
        instance.selectEndpoints({element: ans}).deleteAll();
        delete instance.getManagedElements()[ans.id];
        ans.remove();
        Quest.deleteAnswer(id);
        let answerTable = document.getElementById('anstab' + question.question_id);
        for (const ans of answerTable.childNodes) {
            instance.revalidate(ans);
        }
    }

    static addMovementForMovementBlock(form, question) {
        form.insertAdjacentHTML('beforeend',
            '<div class=\'col-8\'>'+
                '<div class=\'input-group\'>' +
                    '<span class="input-group-text"> Координаты </span>' +
                    '<input type="text" class="form-control" id="moveCoords" ' +
                            'value=' + question.movements[0].place.coords + '>' +
                '</div>'+
            '</div>'+
            '<div class=\'col-8\'>'+
                '<div class=\'input-group\'>' +
                    '<span class="input-group-text"> Радиус(м) </span>' +
                    '<input type="text" class="form-control" id="moveRadius"  ' +
                            'value=' +question.movements[0].place.radius + '>' +
                  '</div>'+
            '</div>'
        );
    }

    static createStartRedactor(form, question) {
        this.addTextRedactor(form, 'Приветственное сообщение:', question.text);
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            Quest.updateQuestion(question.question_id, JSON.stringify({
                type: question.type,
                text: question.text,
            })).then(() => console.log('success'));
        };
    }

    static createFinishRedactor(form, question) {
        this.addTextRedactor(form, 'Прощальное сообщение:', question.text);
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            Quest.updateQuestion(question.question_id, JSON.stringify({
                type: question.type,
                text: question.text,
            })).then(() => console.log('success'));
        };
    }

    static checkboxHandler(chbx_id, element_id, name, text, event, question, instance, sourceEndpoint) {
        if (document.getElementById(chbx_id).checked) {
            if (event.detail === undefined)
                BlockRedactor.addSpecial(element_id, name, text, 0, question, instance, sourceEndpoint);
            else
                BlockRedactor.addSpecial(element_id, name, text, event.detail, question, instance, sourceEndpoint);
        } else
            BlockRedactor.deleteSpecial(name, question, instance);
    }

    static closeQuestionRedactor(newAns, skipState, wrongState, question, instance) {
        for (const ans of newAns){
            BlockRedactor.deleteAnswer(ans, question, instance, false);
        }
        if (document.getElementById('skip').checked != skipState.isActive) {
            document.getElementById('skip').checked = skipState.isActive;
            document.getElementById('skip').dispatchEvent(new CustomEvent('change', { detail: skipState.points }));
        }
        new Promise((resolve) => setTimeout(resolve, 50)).then(() => {
            if (document.getElementById('wrong').checked != wrongState.isActive) {
                document.getElementById('wrong').checked = wrongState.isActive;
                document.getElementById('wrong').dispatchEvent(new CustomEvent('change', { detail: wrongState.points }));
            }
        });
    }

    static createOpenQuestionRedactor(form, question, instance, sourceEndpoint, modal) {
        this.addTextRedactor(form, 'Вопрос', question.text);
        form.insertAdjacentHTML('beforeend', 
            '<hr><label for="formControlTextarea" class="form-label">Ответы:</label>');
        form.insertAdjacentHTML('beforeend', '<div id="OQanswers"></div>');
        form.insertAdjacentHTML('beforeend',
            '<div class="col-12" id="special">' +
                '<div class="form-check pb-1" id="skipChbx">' +
                    '<input class="form-check-input" type="checkbox" id="skip">' +
                    '<label class="form-check-label" for="skip">' +
                        'Добавить возможность пропусить вопрос' +
                    '</label>' +
                '</div>' +
                '<div class="form-check pb-1" id="wrongChbx">' +
                    '<input class="form-check-input" type="checkbox" id="wrong">' +
                    '<label class="form-check-label" for="wrong">' +
                        'Добавить действие в случае неправильного ответа' +
                    '</label>' +
                '</div>' +
                '<div class="col-auto pt-2">' +
                    '<button type="button" class="btn btn-primary" id="addAnswer">' +
                        'Добавить ответ' +
                    '</button>' +
                '</div>' +
            '</div>'
        );
   
        document.getElementById('skip').onchange = (event) => {
            BlockRedactor.checkboxHandler('skip', 'skipChbx', 'skipbx', 'skip', event, question, instance,
                sourceEndpoint);
        }
        document.getElementById('wrong').onchange = (event) => {
            BlockRedactor.checkboxHandler('wrong', 'wrongChbx', 'wrongbx', '', event, question, instance,
                sourceEndpoint);
        }

        let skipState = {
            isActive: false,
            points: 0,
        };
        let wrongState = {
            isActive: false,
            points: 0,
        };
        for (const answer of question.answer_options) {
            if (answer.text === 'skip') {
                BlockRedactor.showSpecial('skipChbx', answer, 'skipbx', 'skip');
                document.getElementById('skip').checked = true;
                skipState.isActive = true;
                skipState.points = answer.points;
                continue;
            }
            if (answer.text === '') {
                BlockRedactor.showSpecial('wrongChbx', answer, 'wrongbx', 'Любой другой ответ');
                document.getElementById('wrong').checked = true;
                wrongState.isActive = true;
                wrongState.points = answer.points;
                continue;
            }
            this.addAnswerForQuestion('OQanswers', answer, question, instance);
        }

        let newAns = [];
        document.getElementById('addAnswer').onclick = () => {
            Quest.addAnswer(JSON.stringify({
                points: 0,
                text: '',
            })).then((response) => {
                const answer = {
                    answer_option_id: JSON.parse(response).answer_option_id,
                    points: 0,
                    text: '',
                };
                question.answer_options.push(answer);
                this.addAnswerForQuestion('OQanswers', answer, question, instance);
                Render.renderAnswer(answer, question, instance, sourceEndpoint);
                newAns.push(answer);
            });
        };
        document.getElementById('close').onclick = () => {
            BlockRedactor.closeQuestionRedactor(newAns, skipState, wrongState, question, instance);
        };
        document.getElementById('xclose').onclick = () => {
            BlockRedactor.closeQuestionRedactor(newAns, skipState, wrongState, question, instance);
        };
        document.getElementById('update').onclick = () => {
            let invalid = false;
            for (const answer of question.answer_options) {
                let ans = document.getElementById('answerText' + answer.answer_option_id);
                if (ans === null)
                    continue;
                if (ans.value === 'skip' || ans.value === '') {
                    ans.className = 'form-control is-invalid';
                    invalid = true;
                } else
                    ans.className = 'form-control';
            }
            if (invalid)
                return false;
            
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            for (const answer of question.answer_options) {
                const answerId = answer.answer_option_id;
                let elem = document.getElementById('answerText' + answerId);
                if (elem !== null) {
                    answer.text = document.getElementById('answerText' + answerId).value;
                    document.getElementById('answer_option' + answerId).innerText = answer.text;
                }
                answer.points = document.getElementById('answerPoints' + answerId).value;
                question.text = document.getElementById('formControlTextarea').value;
                let answerTable = document.getElementById('anstab' + question.question_id);

                for (const ans of answerTable.childNodes)
                    instance.revalidate(ans);
                Quest.updateAnswer(answerId, JSON.stringify({
                    points: answer.points,
                    text: answer.text,
                })).then((response) => console.log(response));
                Quest.updateQuestion(question.question_id, JSON.stringify({
                    type: question.type,
                    text: question.text,
                })).then(() => console.log('success'));
                modal.hide();
            }
        };
    }

    static createMovementRedactor(form, question) {
        BlockRedactor.addTextRedactor(form, 'Перемещение', question.text);
        form.innerHTML+=
        '<div class="z-depth-1-half map-container" style="height: 500px" id="map"></div>';
        let myMap;
        const mapId = document.getElementById('map');
        console.log(mapId);
        ymaps.ready(function() {
            myMap = new ymaps.Map('map', {
                center: [57.5262, 38.3061],
                zoom: 11,
            }, {
                balloonMaxWidth: 200,
                searchControlProvider: 'yandex#search',
            });
            console.log(myMap);
            myMap.events.add('click', function(e) {
                if (!myMap.balloon.isOpen()) {
                    const coords = e.get('coords');
                    myMap.balloon.open(coords, {
                        contentHeader: 'Новое место квеста',
                        contentBody: '<p></p>' +
                            '<p>Координаты точки: ' + [
                            coords[0].toPrecision(6),
                            coords[1].toPrecision(6),
                        ].join(', ') + '</p>',
                        contentFooter: '<sup>Вы можете выбрать новую точку</sup>',
                    });
                    // console.log(coords[0]);
                    question.movements[0].place.coords ='('+coords[0].toString()+','+coords[1].toString()+')';
                    console.log( question.movements[0].place.coords);
                    document.getElementById('moveCoords').value = question.movements[0].place.coords;
                } else {
                    myMap.balloon.close();
                }
            });

            myMap.events.add('balloonopen', function(e) {
                myMap.hint.close();
            }); ;
        });
        console.log(myMap);
        BlockRedactor.addMovementForMovementBlock(form, question);
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            question.movements[0].place.coords = document.getElementById('moveCoords').value;
            question.movements[0].place.radius = document.getElementById('moveRadius').value;
            question.answer_options[0].points = document.getElementById('movePoints').value;
        };
    }

    static showRedactor(question, instance, sourceEndpoint) {
        const modal = new bootstrap.Modal(document.getElementById('redactor'));
        const form = document.getElementById('redactorForm');
        form.innerHTML = '';
        switch (question.type) {
        case 'start':
            BlockRedactor.createStartRedactor(form, question);
            break;
        case 'end':
            BlockRedactor.createFinishRedactor(form, question);
            break;
        case 'open':
            BlockRedactor.createOpenQuestionRedactor(form, question, instance, sourceEndpoint, modal);
            break;
        case 'movement':
            BlockRedactor.createMovementRedactor(form, question);
            break;
        case 'choice':
            // TODO: change this to function for "choice"
            BlockRedactor.createOpenQuestionRedactor(form, question, instance, sourceEndpoint, modal);
            break;
        default:
            break;
        }
        modal.show();
    }
}
