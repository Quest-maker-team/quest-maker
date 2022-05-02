import {Quest} from './quest';
import * as bootstrap from 'bootstrap';
import {Render} from './render';

export class BlockRedactor {
    static addTextRedactor(form, label, text) {
        form.insertAdjacentHTML('beforeend',
            '<label for="formControlTextarea" class="form-label mt-2">' + label + '</label>' +
            '<textarea class="form-control mt-0" id="formControlTextarea" rows="3">' +
                text +
            '</textarea>'
        );
    }

    static addAnswerBox(elementId, state, id, text, points) {
        document.getElementById(elementId).insertAdjacentHTML('beforeend',
            '<div class="row pb-1" id="answer_' + state + '_' + id + '">' +
                '<div class="col-8">' +
                    '<input type="text" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                        'name="answerText_'+ state + '" id="answerText_' + state + '_' + id + '" value="' +
                        text + '" placeholder="Вариант ответа" onclick="document.getElementById(\'answerText_' +
                        state + '_' + id + '\').className = \'form-control\'; return false;">' +
                    '<div class="invalid-feedback">' +
                        'Не используйте "skip" или пустую строку в качестве ответов. ' +
                        'Добавить возможность пропуска можно, установив соответствующий флаг.' +
                    '</div>' +
                '</div>' +
                '<div class="col-3">' +
                    '<div class="input-group">' +
                        '<span class="input-group-text"> Очки </span>' +
                        '<input type="number" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                            'name="answerPoints_'+ state + '" id="answerPoints_' + state + '_' + id + '" value="' +
                            points + '">' +
                    '</div>' +
                '</div>' +
                '<div class="col-1">' +
                    '<button type="button" class="btn btn-danger" id="ansdel_' + state + '_' + id + '">' +
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
        document.getElementById('ansdel_' + state + '_' + id).onclick = () => {
            document.getElementById('answer_' + state + '_' + id).remove();
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

    static addHintBox(elementId, state, id, text, fine) {
        document.getElementById(elementId).insertAdjacentHTML('beforeend',
            '<div class="row pb-1" id="hint_' + state + '_' + id + '">' +
                '<div class="col-8">' +
                    '<textarea class="form-control" name="hintText_' + state + '" id="hintText_' + state + '_'
                            + id + '" rows="1" placeholder="Текст подсказки">' +
                        text +
                    '</textarea>' +
                '</div>' +
                '<div class="col-3">' +
                    '<div class="input-group">' +
                        '<span class="input-group-text"> Штраф </span>' +
                        '<input type="number" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                            'name="hintFine_'+ state + '" id="hintFine_' + state + '_' + id + '" value="' + fine + '">' +
                    '</div>' +
                '</div>' +
                '<div class="col-1">' +
                    '<button type="button" class="btn btn-danger" id="hintdel_' + state + '_' + id + '">' +
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
        document.getElementById('hintdel_' + state + '_' + id).onclick = () => {
            document.getElementById('hint_' + state + '_' + id).remove();
        };
    }

    static loadAnswers(question) {
        let skipActive = false;
        let wrongActive = false;
        let skipPoints = 0;
        let wrongPoints = 0;

        for (const answer of question.answer_options) {
            if (answer.text === 'skip') {
                document.getElementById('skip').checked = true;
                skipActive = true;
                skipPoints = answer.points;
                continue;
            }
            if (answer.text === '') {
                document.getElementById('wrong').checked = true;
                wrongActive = true;
                wrongPoints = answer.points;
                continue;
            }
            BlockRedactor.addAnswerBox('QAnswers', 'old', answer.answer_option_id, answer.text, answer.points);
        }
        BlockRedactor.addSpecialBox('skipChbx', skipPoints, 'skipbx', 'skip', !skipActive);
        BlockRedactor.addSpecialBox('wrongChbx', wrongPoints, 'wrongbx', 'Любой другой ответ', !wrongActive);
    }

    static loadHints(question, elementId) {
        for (const hint of question.hints) {
            BlockRedactor.addHintBox(elementId, 'old', hint.hint_id, hint.hint_text, hint.fine);
        }
    }

    static updateAnswers(question, instance, sourceEndpoint) {
        let idToDel = [];
        for (const answer of question.answer_options) {
            if (answer.text === '' || answer.text === 'skip') {
                continue;
            }
            let elem = document.getElementById('answer_old_' + answer.answer_option_id);
            if (elem === null) {
                const ans = document.getElementById('answer_option' + answer.answer_option_id);
                Render.deleteElemEndpoint(ans, instance);
                ans.remove();
                Quest.deleteEntity('answer_option', answer.answer_option_id);
                idToDel.push(answer.answer_option_id);
            } else {
                answer.text = document.getElementById('answerText_old_' + answer.answer_option_id).value;
                answer.points = document.getElementById('answerPoints_old_' + answer.answer_option_id).value;
                document.getElementById('answer_option' + answer.answer_option_id).innerText = answer.text;
                Quest.updateEntity('answer_option', answer.answer_option_id, JSON.stringify({
                    points: parseFloat(answer.points),
                    text: answer.text,
                }));
            }
        }
        for (const id of idToDel) {
            question.answer_options.splice(question.answer_options.findIndex((answer) =>
                answer.answer_option_id == id), 1);
        }

        let newAnswers = document.getElementsByName('answerText_new');
        for (const newAnswer of newAnswers) {
            let id = newAnswer.id.split('_')[2];
            Quest.addEntity('answer_option', JSON.stringify({
                points: parseFloat(document.getElementById('answerPoints_new_' + id).value),
                text: newAnswer.value,
            })).then((response) => {
                const answer = {
                    answer_option_id: JSON.parse(response).answer_option_id,
                    points: parseFloat(document.getElementById('answerPoints_new_' + id).value),
                    text: newAnswer.value,
                };
                question.answer_options.push(answer);
                Render.renderAnswer(answer, question, instance, sourceEndpoint);
                Quest.connect('question', 'answer_option', question.question_id, answer.answer_option_id);
            });
        }
    }

    static updateSpecial(checkboxId, id, question, instance, text, sourceEndpoint) {
        const specialId = question.answer_options.findIndex((answer) => answer.text === text);
        if (specialId !== -1 && document.getElementById(checkboxId).checked) {
            const answer = question.answer_options[specialId];
            answer.points = document.getElementById('answerPoints' + id).value;
            Quest.updateEntity('answer_option', answer.answer_option_id, JSON.stringify({
                points: parseFloat(answer.points),
                text: answer.text,
            })).then((response) => console.log(response));
            return;
        }
        if (specialId === -1 && !document.getElementById(checkboxId).checked) {
            return;
        }
        if (specialId !== -1) {
            const ans = document.getElementById('answer_option' + question.answer_options[specialId].answer_option_id);
            Render.deleteElemEndpoint(ans, instance);
            ans.remove();
            Quest.deleteEntity('answer_option', question.answer_options[specialId].answer_option_id);
            question.answer_options.splice(specialId, 1);
        } else {
            Quest.addEntity('answer_option', JSON.stringify({
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
                Quest.connect('question', 'answer_option', question.question_id, answer.answer_option_id);
            });
        }
    }

    static updateHints(question) {
        let idToDel = [];
        for (const hint of question.hints) {
            let elem = document.getElementById('hint_old_' + hint.hint_id);
            if (elem === null) {
                Quest.deleteEntity('hint', hint.hint_id);
                idToDel.push(hint.hint_id);
            } else {
                hint.hint_text = document.getElementById('hintText_old_' + hint.hint_id).value;
                hint.fine = document.getElementById('hintFine_old_' + hint.hint_id).value;
                Quest.updateEntity('hint', hint.hint_id, JSON.stringify({
                    fine: parseFloat(hint.fine),
                    text: hint.hint_text,
                }));
            }
        }
        for (const id of idToDel) {
            question.hints.splice(question.hints.findIndex((hint) =>
                    hint.hint_id == id), 1);
        }

        let newHints = document.getElementsByName('hintText_new');
        for (const newHint of newHints) {
            let id = newHint.id.split('_')[2];
            Quest.addEntity('hint', JSON.stringify({
                fine: parseFloat(document.getElementById('hintFine_new_' + id).value),
                text: newHint.value,
            })).then((response) => {
                const hint = {
                    hint_id: JSON.parse(response).hint_id,
                    fine: parseFloat(document.getElementById('hintFine_new_' + id).value),
                    hint_text: newHint.value,
                };
                question.hints.push(hint);
                Quest.connect('question', 'hint', question.question_id, hint.hint_id);
            });
        }
    }

    static validateAnswers() {
        const oldAns = document.getElementsByName('answerText_old');
        const newAns = document.getElementsByName('answerText_new');

        if (oldAns.length === 0 && newAns.length === 0) {
            document.getElementById('ansAlert').hidden = false;
            return false;
        }

        let valid = true;
        for (const ans of oldAns) {
            if (ans.value === 'skip' || ans.value === '') {
                ans.className = 'form-control is-invalid';
                valid = false;
            } else {
                ans.className = 'form-control';
            }
        }
        for (const ans of newAns) {
            if (ans.value === 'skip' || ans.value === '') {
                ans.className = 'form-control is-invalid';
                valid = false;
            } else {
                ans.className = 'form-control';
            }
        }

        return valid;
    }

    static updateQuestion(question, instance, sourceEndpoint) {
        BlockRedactor.updateSpecial('skip', 'skipbx', question, instance, 'skip', sourceEndpoint);
        BlockRedactor.updateSpecial('wrong', 'wrongbx', question, instance, '', sourceEndpoint);

        BlockRedactor.updateAnswers(question, instance, sourceEndpoint);

        BlockRedactor.updateHints(question);

        question.text = document.getElementById('formControlTextarea').value;
        document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
            question.text;
        Quest.updateEntity('question', question.question_id, JSON.stringify({
            type: question.type,
            text: question.text,
        })).then(() => console.log('success'));
    }

    static createQuestionRedactor(form, question, instance, sourceEndpoint, modal) {
        BlockRedactor.addTextRedactor(form, 'Вопрос:', question.text);
        form.insertAdjacentHTML('beforeend',
            '<hr>' +
            '<div class="col-12 mt-0">' +
                '<button type="button" class="accordion-button collapsed p-0" data-bs-toggle="collapse" ' +
                        'data-bs-target="#QHints">' +
                    '<label for="formControlTextarea" class="form-label mt-0">Подсказки:</label>' +
                '</button>' +
            '</div>'
        );
        form.insertAdjacentHTML('beforeend', '<div class="collapse mt-2" id="QHints"></div>');
        form.insertAdjacentHTML('beforeend',
            '<hr class="mt-2">' +
            '<div class="col-12 mt-0">' +
                '<button type="button" class="accordion-button p-0" data-bs-toggle="collapse" ' +
                        'data-bs-target="#QAnswers">' +
                    '<label for="formControlTextarea" class="form-label mt-0">Ответы:</label>' +
                '</button>' +
            '</div>'
        );
        form.insertAdjacentHTML('beforeend', '<div class="collapse show mt-2" id="QAnswers"></div>');
        form.insertAdjacentHTML('beforeend',
            '<div class="alert alert-warning" id="ansAlert" hidden>' +
                'Должен быть хотя бы один вариант ответа' +
            '</div>'
        );
        form.insertAdjacentHTML('beforeend',
            '<hr class="mt-2">' +
            '<div class="col-12 mt-0" id="special">' +
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
                '<div class="row pt-2">' +
                    '<div class="col-auto pr-1">' +
                        '<button type="button" class="btn btn-primary" id="addAnswer">' +
                            'Добавить ответ' +
                        '</button>' +
                    '</div>' +
                    '<div class="col-auto p-0">' +
                        '<button type="button" class="btn btn-primary" id="addHint">' +
                            'Добавить подсказку' +
                        '</button>' +
                    '</div>' +
                '</div>' +
            '</div>'
        );

        document.getElementById('skip').onchange = () => {
            document.getElementById('skipbx').hidden = !document.getElementById('skipbx').hidden;
        };
        document.getElementById('wrong').onchange = () => {
            document.getElementById('wrongbx').hidden = !document.getElementById('wrongbx').hidden;
        };

        BlockRedactor.loadAnswers(question, instance);
        BlockRedactor.loadHints(question, 'QHints');

        let ansId = 0
        document.getElementById('addAnswer').onclick = () => {
            BlockRedactor.addAnswerBox('QAnswers', 'new', ansId, '', 0);
            document.getElementById('ansAlert').hidden = true;
            ansId += 1;
        };
        let hintId = 0;
        document.getElementById('addHint').onclick = () => {
            BlockRedactor.addHintBox('QHints', 'new', hintId, '', 0);
            hintId += 1;
        };
        document.getElementById('update').onclick = () => {
            if (!BlockRedactor.validateAnswers()) {
                return false;
            }

            BlockRedactor.updateQuestion(question, instance, sourceEndpoint);

            Render.updateAnswersEndpoints(question, instance);
            modal.hide();
        };
    }

    static addMovementForMovementBlock(form, question) {
        form.insertAdjacentHTML('beforeend',
            '<div class="col-8">'+
                '<div class="input-group">' +
                    '<span class="input-group-text"> Координаты </span>' +
                    '<input type="text" class="form-control" id="moveCoords" ' +
                            'value=' + question.movements[0].place.coords + '>' +
                '</div>'+
            '</div>'+
            '<div class="col-8">'+
                '<div class="input-group">' +
                    '<span class="input-group-text"> Радиус(м) </span>' +
                    '<input type="text" class="form-control" id="moveRadius"  ' +
                            'value=' + question.movements[0].place.radius + '>' +
                  '</div>'+
            '</div>'
        );
    }

    static createMovementRedactor(form, question, modal) {
        BlockRedactor.addTextRedactor(form, 'Перемещение:', question.text);
        form.insertAdjacentHTML('beforeend',
            '<hr>' +
            '<div class="col-12 mt-0">' +
                '<button type="button" class="accordion-button collapsed p-0" data-bs-toggle="collapse" ' +
                        'data-bs-target="#MHints">' +
                    '<label for="formControlTextarea" class="form-label mt-0">Подсказки:</label>' +
                '</button>' +
            '</div>');
        form.insertAdjacentHTML('beforeend', '<div class="collapse mt-2" id="MHints"></div><hr class="mt-2">');
        form.insertAdjacentHTML('beforeend',
            '<div class="col-auto mt-0">' +
                '<button type="button" class="btn btn-primary" id="addHint">' +
                    'Добавить подсказку' +
                '</button>' +
            '</div>'
        );
        form.insertAdjacentHTML('beforeend',
            '<div class="z-depth-1-half map-container" style="height: 500px" id="map"></div>');
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
        BlockRedactor.loadHints(question, 'MHints');
        let id = 0;
        document.getElementById('addHint').onclick = () => {
            BlockRedactor.addHintBox('MHints', 'new', id, '', 0);
            id += 1;
        };
        document.getElementById('update').onclick = () => {
            BlockRedactor.updateHints(question);
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            question.movements[0].place.coords = document.getElementById('moveCoords').value;
            question.movements[0].place.radius = document.getElementById('moveRadius').value;
            modal.hide();
        };
    }

    static createStartRedactor(form, question, modal) {
        this.addTextRedactor(form, 'Приветственное сообщение:', question.text);
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            Quest.updateEntity('question', question.question_id, JSON.stringify({
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
            Quest.updateEntity('question', question.question_id, JSON.stringify({
                type: question.type,
                text: question.text,
            })).then(() => console.log('success'));
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
            Quest.updateEntity('quest', quest.data.quest_id, JSON.stringify({
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