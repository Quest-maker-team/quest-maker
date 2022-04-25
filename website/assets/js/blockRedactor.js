import {Quest} from './quest';
import * as bootstrap from 'bootstrap';
import {Render} from './render';

export class BlockRedactor {
    static addTextRedactor(form, label, text) {
        form.insertAdjacentHTML('beforeend',
            '<label for="formControlTextarea" class="form-label">' + label + '</label>' +
            '<textarea class="form-control" id="formControlTextarea" rows="3">' +
            text +
            '</textarea>'
        );
    }

    static delete(optionId, elementIdPart, question, instance, special) {
        const ans = document.getElementById('answer_option' + optionId);

        if (!special) {
            document.getElementById(elementIdPart + optionId).remove();
        }

        question.answer_options.splice(question.answer_options.findIndex((ans) =>
            ans.answer_option_id == optionId), 1);
        Render.deleteElemEndpoint(ans, instance);
        ans.remove();
        Quest.deleteEntity('answer_option', optionId);
        Render.updateAnswersEndpoints(question, instance);
    }

    static deleteAnswer(answer, question, instance, withConfirm) {
        let conf = true;
        if (withConfirm) {
            conf = confirm('Вы действительно хотите удалить вариант ответа? Отменить действие будет не возможно.');
        }
        if (conf) {
            BlockRedactor.delete(answer.answer_option_id, 'ansblock', question, instance, false);
        }
    }

    static addAnswerForQuestion(elementId, answer, question, instance) {
        document.getElementById(elementId).insertAdjacentHTML('beforeend',
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
            BlockRedactor.deleteAnswer(answer, question, instance, true);
        };
    }

    static addSpecialBox(elementId, points, id, text, hide) {
        document.getElementById(elementId).insertAdjacentHTML('afterend',
            '<div class="row pb-1" id="' + id + '"' + (hide ? ' hidden' : '') + '>' +
                '<div class="col-8">'+
                    '<input type="text" class="form-control" placeholder="' + text + '" readonly>' +
                '</div>' +
                '<div class="col-3">' +
                    '<div class="input-group">' +
                        '<span class="input-group-text"> Очки </span>' +
                        '<input type="number" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                            'id="answerPoints' + id + '" value="' + points + '">' +
                    '</div>' +
                '</div>' +
            '</div>'
        );
    }

    static updateSpecialState(state, checkboxId, id, question, instance, text, sourceEndpoint) {
        if (state.isActive === document.getElementById(checkboxId).checked) {
            if (state.isActive) {
                const answer = question.answer_options[question.answer_options.findIndex((ans) =>
                    ans.answer_option_id == state.id)];
                answer.points = document.getElementById('answerPoints' + id).value;
                Quest.updateAnswer(state.id, JSON.stringify({
                    points: parseFloat(answer.points),
                    text: answer.text,
                })).then((response) => console.log(response));
            }
            return;
        }
        if (state.isActive) {
            BlockRedactor.delete(state.id, '', question, instance, true);
        } else {
            Quest.addAnswer(JSON.stringify({
                points: parseFloat(document.getElementById('answerPoints' + id).value),
                text: text,
            })).then((response) => {
                const answer = {
                    answer_option_id: JSON.parse(response).answer_option_id,
                    points: parseFloat(document.getElementById('answerPoints' + id).value),
                    text: text,
                };
                question.answer_options.push(answer);
                Render.renderAnswer(answer, question, instance, sourceEndpoint, true);
                return Quest.connect('question', 'answer_option', question.question_id, answer.answer_option_id);
            }).then(result => console.log('special pidor'));
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
                            'value=' + question.movements[0].place.radius + '>' +
                  '</div>'+
            '</div>'
        );
    }

    static createStartRedactor(form, question, modal) {
        this.addTextRedactor(form, 'Приветственное сообщение:', question.text);
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            Quest.updateQuestion(question.question_id, JSON.stringify({
                type: question.type,
                text: question.text,
            })).then(() => console.log('success'));
            modal.hide();
        };
    }

    static createFinishRedactor(form, question, modal) {
        this.addTextRedactor(form, 'Прощальное сообщение:', question.text);
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            Quest.updateQuestion(question.question_id, JSON.stringify({
                type: question.type,
                text: question.text,
            })).then(() => console.log('success'));
            modal.hide();
        };
    }

    static loadAnswers(question, instance) {
        const specialStates = {
            skip: {
                id: undefined,
                isActive: false,
            },
            wrong: {
                id: undefined,
                isActive: false,
            },
        };
        let skipPoints = 0;
        let wrongPoints = 0;

        for (const answer of question.answer_options) {
            if (answer.text === 'skip') {
                document.getElementById('skip').checked = true;
                specialStates.skip.id = answer.answer_option_id;
                specialStates.skip.isActive = true;
                skipPoints = answer.points;
                continue;
            }
            if (answer.text === '') {
                document.getElementById('wrong').checked = true;
                specialStates.wrong.id = answer.answer_option_id;
                specialStates.wrong.isActive = true;
                wrongPoints = answer.points;
                continue;
            }
            BlockRedactor.addAnswerForQuestion('OQanswers', answer, question, instance);
        }
        BlockRedactor.addSpecialBox('skipChbx', skipPoints, 'skipbx', 'skip', !specialStates.skip.isActive);
        BlockRedactor.addSpecialBox('wrongChbx', wrongPoints, 'wrongbx', 'Любой другой ответ',
            !specialStates.wrong.isActive);

        return specialStates;
    }

    static validateAnswers(question) {
        let valid = true;

        for (const answer of question.answer_options) {
            const ans = document.getElementById('answerText' + answer.answer_option_id);
            if (ans === null) {
                continue;
            }
            if (ans.value === 'skip' || ans.value === '') {
                ans.className = 'form-control is-invalid';
                valid = false;
            } else {
                ans.className = 'form-control';
            }
        }

        return valid;
    }

    static updateOpenQuestion(question, specialState, instance, sourceEndpoint) {
        console.log(specialState);
        BlockRedactor.updateSpecialState(specialState.skip, 'skip', 'skipbx', question, instance, 'skip',
            sourceEndpoint);

        for (const answer of question.answer_options) {
            const answerId = answer.answer_option_id;
            if (document.getElementById('answerText' + answerId) === null) {
                continue;
            }

            answer.text = document.getElementById('answerText' + answerId).value;
            document.getElementById('answer_option' + answerId).innerText = answer.text;
            answer.points = document.getElementById('answerPoints' + answerId).value;

            Quest.updateAnswer(answerId, JSON.stringify({
                points: parseFloat(answer.points),
                text: answer.text,
            })).then((response) => console.log(response));
        }

        BlockRedactor.updateSpecialState(specialState.wrong, 'wrong', 'wrongbx', question, instance, '',
            sourceEndpoint);

        question.text = document.getElementById('formControlTextarea').value;
        document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
            question.text;
        Quest.updateQuestion(question.question_id, JSON.stringify({
            type: question.type,
            text: question.text,
        })).then(() => console.log('success'));
    }

    static createQuestionRedactor(form, question, instance, sourceEndpoint, modal) {
        BlockRedactor.addTextRedactor(form, 'Вопрос', question.text);
        form.insertAdjacentHTML('beforeend',
            '<hr><label for="formControlTextarea" class="form-label">Ответы:</label>');
        form.insertAdjacentHTML('beforeend', '<div id="OQanswers"></div>');
        form.insertAdjacentHTML('beforeend',
            '<div class="col-12" id="special">' +
                '<div class="form-check pb-1" id="skipChbx">' +
                    '<input class="form-check-input" type="checkbox" id="skip">' +
                    '<label class="form-check-label" for="skip">' +
                        'Добавить возможность пропустить вопрос' +
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

        document.getElementById('skip').onchange = () => {
            document.getElementById('skipbx').hidden = !document.getElementById('skipbx').hidden;
        };
        document.getElementById('wrong').onchange = () => {
            document.getElementById('wrongbx').hidden = !document.getElementById('wrongbx').hidden;
        };

        const specialState = BlockRedactor.loadAnswers(question, instance);

        const newAns = [];
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
                BlockRedactor.addAnswerForQuestion('OQanswers', answer, question, instance);
                Render.renderAnswer(answer, question, instance, sourceEndpoint);
                newAns.push(answer);
                return Quest.connect('question', 'answer_option', question.question_id, answer.answer_option_id);
            }).then(result => console.log('pidor'));
        };
        document.getElementById('close').onclick = () => {
            for (const ans of newAns) {
                BlockRedactor.deleteAnswer(ans, question, instance, false);
            }
        };
        document.getElementById('xclose').onclick = () => {
            for (const ans of newAns) {
                BlockRedactor.deleteAnswer(ans, question, instance, false);
            }
        };
        document.getElementById('update').onclick = () => {
            if (!BlockRedactor.validateAnswers(question)) {
                return false;
            }

            BlockRedactor.updateOpenQuestion(question, specialState, instance, sourceEndpoint);

            Render.updateAnswersEndpoints(question, instance);
            modal.hide();
        };
    }

    static createMovementRedactor(form, question, modal) {
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
            modal.hide();
        };
    }

    static showRedactor(question, instance, sourceEndpoint) {
        const modal = new bootstrap.Modal(document.getElementById('redactor'));
        const form = document.getElementById('redactorForm');
        form.innerHTML = '';
        switch (question.type) {
        case 'start':
            BlockRedactor.createStartRedactor(form, question, modal);
            break;
        case 'end':
            BlockRedactor.createFinishRedactor(form, question, modal);
            break;
        case 'open':
            BlockRedactor.createQuestionRedactor(form, question, instance, sourceEndpoint, modal);
            break;
        case 'movement':
            BlockRedactor.createMovementRedactor(form, question, modal);
            break;
        case 'choice':
            BlockRedactor.createQuestionRedactor(form, question, instance, sourceEndpoint, modal);
            break;
        default:
            break;
        }
        modal.show();
    }
}


export class QuestRedactor{
    static createQuestRedactor(form, quest) {
        form.insertAdjacentHTML('beforeend',
            '<div class="col-12" id="special">' +
                    '<label class="form-check-label" for="questTitle">' +
                        'Название квеста' +
                    '</label>' +
                    '<input type="text" onkeydown="return (event.keyCode!=13);" class="form-control" id="questTitle"' +
                        ' value="' + quest.data.title + '" placeholder="Название квеста">' +

                    '<label for="formControlTextarea" class="form-label mt-2">' + 'Описание' + '</label>' +
                    '<textarea class="form-control" id="questDescription" rows="3">' +
                        quest.data.description +
                    '</textarea>' +

                    '<div  class="form-check mt-2">' +
                        '<input class="form-check-input" type="checkbox" id="private" ' +
                        (quest.data.password.toString() !== '' ? 'checked' : '') + '>' +
                        '<label class="form-check-label" for="private">' +
                            'Приватный квест' +
                        '</label>' +
                    '</div>' +

                    '<div id="passwordBox" ' +
                        (quest.data.password.toString() === '' ? 'hidden' : '') + '>' +
                        '<label class="form-check-label" for="private">' +
                            'Ключевое слово' +
                        '</label>' +
                        '<input type="text" onkeydown="return (event.keyCode!=13);" class="form-control" id="questPassword"' +
                            ' value="' + quest.data.password + '" placeholder="Ключевое слово">' +
                    '</div>' +
            '</div>'
        );
    }

    static showQuestRedactor(quest) {
        const modal = new bootstrap.Modal(document.getElementById('redactor'));
        const form = document.getElementById('redactorForm');
        form.innerHTML = '';

        QuestRedactor.createQuestRedactor(form, quest);

        document.getElementById('private').onchange = () => {
            document.getElementById('passwordBox').hidden = !document.getElementById('passwordBox').hidden;
        };

        document.getElementById('update').onclick = () => {
            Quest.updateQuest(quest.data.quest_id, JSON.stringify({
                title: document.getElementById('questTitle').value,
                description: document.getElementById('questDescription').value,
                password: document.getElementById('private').checked ? document.getElementById('questPassword').value : '',
            }));

            quest.data.title = document.getElementById('questTitle').value;
            quest.data.description = document.getElementById('questDescription').value;
            quest.data.password = document.getElementById('private').checked ? document.getElementById('questPassword').value : '';

            modal.hide();
        }

        modal.show();
    }
}
