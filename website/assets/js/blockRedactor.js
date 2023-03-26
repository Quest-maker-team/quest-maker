import {Quest} from './quest';
import * as bootstrap from 'bootstrap';
import _ from 'underscore';
import {Render} from './render';

export class BlockRedactor {
    static addTextRedactor(form, label, text) {
        form.insertAdjacentHTML('beforeend',
            '<label for="formControlTextarea" class="form-label mt-2">' + label + '</label>' +
            '<textarea class="form-control mt-0" id="formControlTextarea" rows="3" ' +
                    'onclick="document.getElementById(\'formControlTextarea\').className = ' +
                    '\'form-control mt-0\'; return false;">' +
                text +
            '</textarea>' +
            '<div class="invalid-feedback">' +
                'Не используйте пустую строку в качестве вопроса. ' +
            '</div>'
        );
    }

    static addAnswerBox(elementId, isNew, id, text, points) {
        const state = isNew ? 'new' : 'old';
        document.getElementById(elementId).insertAdjacentHTML('beforeend',
            '<div class="row pb-1" id="answer_' + state + '_' + id + '">' +
                '<div class="col-8">' +
                    '<input type="text" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                        'name="answerText_'+ state + '" id="answerText_' + state + '_' + id + '" value="' +
                        _.escape(text) + '" placeholder="Вариант ответа" onclick="document.getElementById(\'' +
                        'answerText_' + state + '_' + id + '\').className = \'form-control\'; return false;">' +
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
                '<div class="col-8">' +
                    '<input type="text" class="form-control" placeholder="' + _.escape(text) + '" readonly>' +
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

    static addHintBox(elementId, isNew, id, text, fine) {
        const state = isNew ? 'new' : 'old';
        document.getElementById(elementId).insertAdjacentHTML('beforeend',
            '<div class="row pb-1" id="hint_' + state + '_' + id + '">' +
                '<div class="col-8">' +
                    '<textarea class="form-control" name="hintText_' + state + '" id="hintText_' + state + '_' +
                            id + '" rows="1" placeholder="Текст подсказки" onclick="document.getElementById(' +
                            '\'hintText_' + state + '_' + id + '\').className = \'form-control\'; return false;">' +
                        _.escape(text) +
                    '</textarea>' +
                    '<div class="invalid-feedback">' +
                        'Не используйте пустую строку в качестве подсказки. ' +
                    '</div>' +
                '</div>' +
                '<div class="col-3">' +
                    '<div class="input-group">' +
                        '<span class="input-group-text"> Штраф </span>' +
                        '<input type="number" onkeydown="return (event.keyCode!=13);" class="form-control" ' +
                            'name="hintFine_'+ state + '" id="hintFine_' + state + '_' + id +
                            '" value="' + fine + '">' +
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

        for (const answer of question.answers) {
            console.log(answer);
            if (answer.text === 'skip') {
                document.getElementById('skip').checked = true;
                skipActive = true;
                skipPoints = answer.points;
            } else if (answer.text === '') {
                document.getElementById('wrong').checked = true;
                wrongActive = true;
                wrongPoints = answer.points;
            } else {
                BlockRedactor.addAnswerBox('QAnswers', false, answer.answer_option_id, answer.text, answer.points);
            }
        }
        BlockRedactor.addSpecialBox('skipChbx', skipPoints, 'skipbx', 'skip', !skipActive);
        BlockRedactor.addSpecialBox('wrongChbx', wrongPoints, 'wrongbx', 'Любой другой ответ', !wrongActive);
    }

    static loadHints(question, elementId) {
        for (const hint of question.hints) {
            BlockRedactor.addHintBox(elementId, false, hint.hint_id, hint.hint_text, hint.fine);
        }
    }

    static updateBlockText(questBlock) {
        questBlock.block_text = document.getElementById('formControlTextarea').value;
        document.getElementById(questBlock.block_id).getElementsByClassName('card-text')[0].textContent =
            questBlock.block_text;
        Quest.updateBlock(questBlock.block_id, JSON.stringify({
            block_text: questBlock.block_text,
        }));
    }

    static updateAnswers(question, instance, sourceEndpoint) {
        const idToDel = [];
        for (const answer of question.answers) {
            if (answer.text !== '' && answer.text !== 'skip') {
                const elem = document.getElementById('answer_old_' + answer.answer_option_id);
                if (elem === null) {
                    idToDel.push(answer.answer_option_id);
                } else {
                    answer.text = document.getElementById('answerText_old_' + answer.answer_option_id).value;
                    answer.points = document.getElementById('answerPoints_old_' + answer.answer_option_id).value;
                    document.getElementById('answer_option' + answer.answer_option_id).innerText = answer.text;
                    Quest.updateEntity('answer_option', answer.answer_option_id, question.block_id, JSON.stringify({
                        points: parseFloat(answer.points),
                        text: answer.text,
                    }));
                }
            }
        }
        for (const id of idToDel) {
            const ans = document.getElementById('answer_option' + id);
            Render.deleteElemEndpoint(ans, instance);
            ans.remove();
            Quest.deleteBlockEntity('answer_option', question.block_id, id);
            question.answers.splice(question.answers.findIndex((answer) =>
                answer.answer_option_id == id), 1);
        }

        const newAnswers = document.getElementsByName('answerText_new');
        for (const newAnswer of newAnswers) {
            const id = newAnswer.id.split('_')[2];
            Quest.addBlockEntity('answer_option', question.block_id, JSON.stringify({
                points: parseFloat(document.getElementById('answerPoints_new_' + id).value),
                text: newAnswer.value,
            })).then((response) => {
                const answer = {
                    answer_option_id: JSON.parse(response).answer_option_id,
                    points: parseFloat(document.getElementById('answerPoints_new_' + id).value),
                    text: newAnswer.value,
                };
                question.answers.push(answer);
                Render.renderAnswer(answer, question, instance, sourceEndpoint);
            });
        }
    }

    static updateSpecial(checkboxId, id, question, instance, text, sourceEndpoint) {
        console.log(question);
        const specialId = question.answers.findIndex((answer) => answer.text === text);
        if (specialId !== -1 && document.getElementById(checkboxId).checked) {
            const answer = question.answers[specialId];
            answer.points = document.getElementById('answerPoints' + id).value;
            Quest.updateEntity('answer_option', answer.answer_option_id, question.block_id, JSON.stringify({
                points: parseFloat(answer.points),
                text: answer.text,
            })).then((response) => console.log(response));
        } else if (specialId !== -1 && !document.getElementById(checkboxId).checked) {
            const ans = document.getElementById('answer_option' + question.answers[specialId].answer_option_id);
            Render.deleteElemEndpoint(ans, instance);
            ans.remove();
            Quest.deleteBlockEntity('answer_option', question.block_id, question.answers[specialId].answer_option_id);
            question.answers.splice(specialId, 1);
        } else if (specialId === -1 && document.getElementById(checkboxId).checked) {
            Quest.addBlockEntity('answer_option', question.block_id, JSON.stringify({
                points: parseFloat(document.getElementById('answerPoints' + id).value),
                text: text,
            })).then((response) => {
                const answer = {
                    answer_option_id: JSON.parse(response).answer_option_id,
                    points: parseFloat(document.getElementById('answerPoints' + id).value),
                    text: text,
                };
                question.answers.push(answer);
                Render.renderAnswer(answer, question, instance, sourceEndpoint, true);
            });
        }
    }

    static updateHints(question) {
        const idToDel = [];
        for (const hint of question.hints) {
            const elem = document.getElementById('hint_old_' + hint.hint_id);
            if (elem === null) {
                idToDel.push(hint.hint_id);
            } else {
                hint.hint_text = document.getElementById('hintText_old_' + hint.hint_id).value;
                hint.fine = document.getElementById('hintFine_old_' + hint.hint_id).value;
                Quest.updateEntity('hint', hint.hint_id, question.block_id, JSON.stringify({
                    fine: parseFloat(hint.fine),
                    hint_text: hint.hint_text,
                }));
            }
        }
        for (const id of idToDel) {
            Quest.deleteBlockEntity('hint', question.block_id, id);
            question.hints.splice(question.hints.findIndex((hint) =>
                hint.hint_id == id), 1);
        }

        const newHints = document.getElementsByName('hintText_new');
        for (const newHint of newHints) {
            const id = newHint.id.split('_')[2];
            Quest.addBlockEntity('hint', question.block_id, JSON.stringify({
                fine: parseFloat(document.getElementById('hintFine_new_' + id).value),
                hint_text: newHint.value,
            })).then((response) => {
                const hint = {
                    hint_id: JSON.parse(response).hint_id,
                    fine: parseFloat(document.getElementById('hintFine_new_' + id).value),
                    hint_text: newHint.value,
                };
                question.hints.push(hint);
            });
        }
    }

    static updatePlace(question, coords, radius) {
        question.movements[0].place.coords = coords;
        question.movements[0].place.radius = radius;
        Quest.updateEntity('place', question.movements[0].place.place_id, question.block_id, JSON.stringify({
            coords: coords,
            radius: radius,
        })).catch((result) => console.log(result));
    }

    static validateAnswers() {
        const answers = document.querySelectorAll('input[name="answerText_old"], input[name="answerText_new"]');

        if (answers.length === 0) {
            document.getElementById('ansAlert').hidden = false;
            return false;
        }

        let valid = true;
        for (const ans of answers) {
            if (ans.value === 'skip' || ans.value === '') {
                ans.className = 'form-control is-invalid';
                valid = false;
            } else {
                ans.className = 'form-control';
            }
        }

        if (!valid) {
            document.getElementById('answersAccordion').className = 'accordion-button p-0';
            document.getElementById('QAnswers').className = 'collapse show mt-2';
        }

        return valid;
    }

    static validateHints(accordionId, collapseId) {
        const hints = document.querySelectorAll('textarea[name="hintText_old"], textarea[name="hintText_new"]');
        let valid = true;

        for (const hint of hints) {
            if (hint.value === '') {
                hint.className = 'form-control is-invalid';
                valid = false;
            } else {
                hint.className = 'form-control';
            }
        }

        if (!valid) {
            document.getElementById(accordionId).className = 'accordion-button p-0';
            document.getElementById(collapseId).className = 'collapse show mt-2';
        }

        return valid;
    }

    static validateQuestion() {
        const question = document.getElementById('formControlTextarea');

        if (question.value === '') {
            question.className = 'form-control mt-0 is-invalid';
            return false;
        } else {
            question.className = 'form-control mt-0';
            return true;
        }
    }

    static updateQuestion(question, instance, sourceEndpoint) {
        BlockRedactor.updateSpecial('skip', 'skipbx', question, instance, 'skip', sourceEndpoint);
        BlockRedactor.updateSpecial('wrong', 'wrongbx', question, instance, '', sourceEndpoint);
        BlockRedactor.updateAnswers(question, instance, sourceEndpoint);
        BlockRedactor.updateHints(question);
        BlockRedactor.updateBlockText(question);
    }

    static createQuestionRedactor(form, question, instance, sourceEndpoint, modal) {
        BlockRedactor.addTextRedactor(form, 'Вопрос:', question.block_text);
        form.insertAdjacentHTML('beforeend',
            '<hr>' +
            '<div class="col-12 mt-0">' +
                '<button type="button" class="accordion-button collapsed p-0" data-bs-toggle="collapse" ' +
                        'data-bs-target="#QHints" style="box-shadow: none !important; ' +
                        'background-color: white !important; color: black !important" ' +
                        'id="hintsAccordion">' +
                    '<label for="formControlTextarea" class="form-label mt-0">Подсказки:</label>' +
                '</button>' +
            '</div>'
        );
        form.insertAdjacentHTML('beforeend', '<div class="collapse mt-2" id="QHints"></div>');
        form.insertAdjacentHTML('beforeend',
            '<hr class="mt-2">' +
            '<div class="col-12 mt-0">' +
                '<button type="button" class="accordion-button p-0" data-bs-toggle="collapse" ' +
                        'data-bs-target="#QAnswers" style="box-shadow: none !important; ' +
                        'background-color: white !important; color: black !important" ' +
                        'id="answersAccordion">' +
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
            '</div>'
        );

        BlockRedactor.loadAnswers(question, instance);
        BlockRedactor.loadHints(question, 'QHints');

        document.getElementById('skip').onchange = () => {
            document.getElementById('skipbx').hidden = !document.getElementById('skipbx').hidden;
        };
        document.getElementById('wrong').onchange = () => {
            document.getElementById('wrongbx').hidden = !document.getElementById('wrongbx').hidden;
        };
        let ansId = 0;
        document.getElementById('addAnswer').onclick = () => {
            BlockRedactor.addAnswerBox('QAnswers', true, ansId, '', 0);
            document.getElementById('ansAlert').hidden = true;
            document.getElementById('answersAccordion').className = 'accordion-button p-0';
            document.getElementById('QAnswers').className = 'collapse show mt-2';
            ansId += 1;
        };
        let hintId = 0;
        document.getElementById('addHint').onclick = () => {
            BlockRedactor.addHintBox('QHints', true, hintId, '', 0);
            document.getElementById('hintsAccordion').className = 'accordion-button p-0';
            document.getElementById('QHints').className = 'collapse show mt-2';
            hintId += 1;
        };
        document.getElementById('update').onclick = () => {
            if (!(BlockRedactor.validateQuestion() && BlockRedactor.validateAnswers() &&
                    BlockRedactor.validateHints('hintsAccordion', 'QHints'))) {
                return false;
            } else {
                BlockRedactor.updateQuestion(question, instance, sourceEndpoint);

                Render.updateAnswersEndpoints(question, instance);
                modal.hide();
            }
        };
    }

    static addOldPlaces(myMap, quest, newQuestion) {
        const questions = quest.data.questions.filter((question) =>
            question.question_id !== newQuestion.question_id && question.type === 'movement');
        for (const question of questions) {
            if (typeof(question.movements[0].place.coords) == 'string') {
                const s = question.movements[0].place.coords.split(',');
                const x = s[0].substring(1);
                const y = s[1].substring(0, s[1].length - 1);
                question.movements[0].place.coords = [parseFloat(x), parseFloat(y)];
            }
            const placeMark = new ymaps.Placemark(question.movements[0].place.coords, {
                balloonContentHeader: 'Добавленное место квеста',
                balloonContentBody:
                    question.text,
            }, {
                preset: 'islands#blueDotIconWithCaption',
                draggable: false,
            });
            const myCircle = new ymaps.Circle([
                question.movements[0].place.coords,
                question.movements[0].place.radius,
            ], {
                hintContent: 'Радиус достижимости ' + question.movements[0].place.radius,
            }, {
                draggable: false,
                fillColor: '#DB709377',
                strokeColor: '#00FA9A',
                strokeOpacity: 0.8,
                strokeWidth: 3,
            });
            myMap.geoObjects.add(myCircle);
            myMap.geoObjects.add(placeMark);
        }
    }

    static addMethodsToMap(myMap, question, radius, coordinates) {
        if (question.movements[0].place.radius>0) {
            radius.value = question.movements[0].place.radius;
        } else {
            coordinates.value = myMap.getCenter();
            radius.value = 25;
        }
        const myCircle = new ymaps.Circle([
            myMap.getCenter(),
            radius.value,
        ], {
            balloonContentHeader: 'Редактируемое место квеста',
            balloonContentBody:
                '<p>' +
                 'Для изменения координат - кликните в любом месте или перетащите круг' +
                 '</p>',
            balloonContentFooter: 'Вы можете посмотеть информацию о других точках кликнув по ним',
            hintContent: 'Радиус достижимости ',
        },
        {
            draggable: true,
            fillColor: '#DB709377',
            strokeColor: '#990066',
            strokeOpacity: 0.8,
            strokeWidth: 3,
        });
        const changeGeometry = (e) => {
            const coords = e.get('target').geometry.getCoordinates();
            radius.value = myCircle.geometry.getRadius();
            coordinates.value = coords;
            if (myCircle.balloon.isOpen()) {
                myCircle.balloon.setPosition(coords);
            }
        };
        const changePosition = (e) => {
            const coords = e.get('coords');
            myMap.geoObjects.get(myMap.geoObjects.indexOf(myCircle)).geometry.setCoordinates(coords);
            coordinates.value = coords;
        };
        myMap.events.add('click', changePosition );
        myCircle.events.add('geometrychange', changeGeometry);
        myMap.geoObjects.add(myCircle);
        myCircle.editor.startEditing();
        myMap.geoObjects.get(myMap.geoObjects.indexOf(myCircle)).balloon.open();
    }

    static createMovementRedactor(form, question, modal, quest) {
        if (typeof(question.movements[0].place.coords)=='string' ) {
            const s = question.movements[0].place.coords.split(',');
            const x = s[0].substring(1);
            const y = s[1].substring(0, s[1].length-1);

            question.movements[0].place.coords = [parseFloat(x), parseFloat(y)];
        }
        BlockRedactor.addTextRedactor(form, 'Перемещение:', question.block_text);
        form.insertAdjacentHTML('beforeend',
            '<hr>' +
            '<div class="col-12 mt-0">' +
                '<button type="button" class="accordion-button collapsed p-0" data-bs-toggle="collapse" ' +
                        'data-bs-target="#MHints" style="box-shadow: none !important; ' +
                        'background-color: white !important; color: black !important" ' +
                        'id="hintsAccordion">' +
                    '<label for="formControlTextarea" class="form-label mt-0">Подсказки:</label>' +
                '</button>' +
            '</div>'
        );
        form.insertAdjacentHTML('beforeend', '<div class="collapse mt-2" id="MHints"></div><hr class="mt-2">');
        form.insertAdjacentHTML('beforeend',
            '<div class="z-depth-1-half map-container" style="height: 500px" id="map"></div>');
        let myMap;
        const radius = {'value': question.movements[0].place.radius};
        const coordinates = {'value': question.movements[0].place.coords};
        ymaps.ready(() => {
            const geolocation = ymaps.geolocation;
            let myPosition;
            geolocation.get({
                provider: 'yandex',
                mapStateAutoApply: true,
            }).then((result) => {
                myPosition = result.geoObjects.position;
                geolocation.get({
                    provider: 'browser',
                    mapStateAutoApply: true,
                }).then((position) => {
                    if (position !== undefined && question.movements[0].place.radius == 0.0) {
                        myPosition = position.geoObjects.position;
                        myMap.setCenter(myPosition);
                        myMap.geoObjects.get(0).setCoordinates(myPosition);
                        myMap.geoObjects.get(1).setCoordinates(myPosition);
                    }
                });

                if (question.movements[0].place.radius > 0.0) {
                    myPosition = question.movements[0].place.coords;
                }
                myMap = new ymaps.Map('map', {
                    center: myPosition,
                    zoom: 11,
                }, {
                    balloonMaxWidth: 200,
                    searchControlProvider: 'yandex#search',

                });
                BlockRedactor.addMethodsToMap(myMap, question, radius, coordinates);
                BlockRedactor.addOldPlaces(myMap, quest, question);
                BlockRedactor.loadHints(question, 'MHints');
            });
        });

        let id = 0;
        document.getElementById('addHint').onclick = () => {
            BlockRedactor.addHintBox('MHints', 'new', id, '', 0);
            document.getElementById('hintsAccordion').className = 'accordion-button p-0';
            document.getElementById('MHints').className = 'collapse show mt-2';
            id += 1;
        };
        document.getElementById('update').onclick = () => {
            if (!(BlockRedactor.validateQuestion() && BlockRedactor.validateHints('hintsAccordion', 'MHints'))) {
                return false;
            } else {
                BlockRedactor.updateHints(question);
                BlockRedactor.updateBlockText(question);
                BlockRedactor.updatePlace(question, coordinates.value, radius.value);
                modal.hide();
            }
        };
    }

    static createStartRedactor(form, questBlock, modal) {
        this.addTextRedactor(form, 'Приветственное сообщение:', questBlock.block_text);
        document.getElementById('update').onclick = () => {
            BlockRedactor.updateBlockText(questBlock);
            modal.hide();
        };
    }

    static createFinishRedactor(form, questBlock, modal) {
        this.addTextRedactor(form, 'Прощальное сообщение:', questBlock.block_text);
        document.getElementById('update').onclick = () => {
            BlockRedactor.updateBlockText(questBlock);
            modal.hide();
        };
    }

    static showRedactor(questBlock, instance, sourceEndpoint, quest) {
        const modal = new bootstrap.Modal(document.getElementById('redactor'));
        const form = document.getElementById('redactorForm');
        form.innerHTML = '';
        const buttons = document.getElementById('modalButtons');
        if (buttons !== null) {
            buttons.remove();
        }
        switch (questBlock.block_type_name) {
        case 'start_block':
            document.getElementById('content').insertAdjacentHTML('beforeend',
                '<div class="modal-footer" id="modalButtons">' +
                    '<button type="button" class="btn btn-secondary" style="margin-right: 0.25em" ' +
                        'data-bs-dismiss="modal" id="close">Закрыть</button>' +
                    '<button type="button" class="btn btn-primary" id="update">Сохранить</button>' +
                '</div>'
            );
            BlockRedactor.createStartRedactor(form, questBlock, modal);
            break;
        case 'end_block':
            document.getElementById('content').insertAdjacentHTML('beforeend',
                '<div class="modal-footer" id="modalButtons">' +
                    '<button type="button" class="btn btn-secondary" style="margin-right: 0.25em" ' +
                        'data-bs-dismiss="modal" id="close">Закрыть</button>' +
                    '<button type="button" class="btn btn-primary" id="update">Сохранить</button>' +
                '</div>'
            );
            BlockRedactor.createFinishRedactor(form, questBlock, modal);
            break;
        case 'open_question':
        case 'choice_question':
            document.getElementById('content').insertAdjacentHTML('beforeend',
                '<div class="modal-footer justify-content-between" id="modalButtons">' +
                    '<div>' +
                        '<button type="button" class="btn btn-primary" id="addAnswer">' +
                            'Добавить ответ' +
                        '</button>' +
                        '<button type="button" class="btn btn-primary" style="margin-left: 0.25em" id="addHint">' +
                            'Добавить подсказку' +
                        '</button>' +
                    '</div>' +
                    '<div>' +
                        '<button type="button" class="btn btn-secondary" style="margin-right: 0.25em" ' +
                            'data-bs-dismiss="modal" id="close">Закрыть</button>' +
                        '<button type="button" class="btn btn-primary" id="update">Сохранить</button>' +
                    '<div>' +
                '</div>'
            );
            BlockRedactor.createQuestionRedactor(form, questBlock, instance, sourceEndpoint, modal);
            break;
        case 'movement':
            document.getElementById('content').insertAdjacentHTML('beforeend',
                '<div class="modal-footer justify-content-between" id="modalButtons">' +
                    '<button type="button" class="btn btn-primary" id="addHint">' +
                        'Добавить подсказку' +
                    '</button>' +
                    '<div>' +
                        '<button type="button" class="btn btn-secondary" style="margin-right: 0.25em" ' +
                            'data-bs-dismiss="modal" id="close">Закрыть</button>' +
                        '<button type="button" class="btn btn-primary" id="update">Сохранить</button>' +
                    '<div>' +
                '</div>'
            );
            BlockRedactor.createMovementRedactor(form, questBlock, modal, quest);
            break;
        default:
            break;
        }
        modal.show();
    }
}


export class QuestRedactor {
    static createQuestRedactor(form, quest) {
        form.insertAdjacentHTML('beforeend',
            '<div class="col-12" id="special">' +
                    '<label class="form-check-label" for="questTitle">' +
                        'Название квеста' +
                    '</label>' +
                    '<input type="text" autocomplete="off" onkeydown="return (event.keyCode!=13);" ' +
                        'class="form-control" id="questTitle"' + ' value="' +
                        _.escape(quest.data.title) + '" placeholder="Название квеста">' +

                    '<label for="formControlTextarea" class="form-label mt-2">' + 'Описание' + '</label>' +
                    '<textarea class="form-control" id="questDescription" rows="3" placeholder="Описание квеста">' +
                        (quest.data.description !== null ? quest.data.description : '') +
                    '</textarea>' +

                    '<div  class="form-check mt-2">' +
                        '<input class="form-check-input" type="checkbox" id="private" ' +
                        (quest.data.password !== null ? 'checked' : '') + '>' +
                        '<label class="form-check-label" for="private">' +
                            'Приватный квест' +
                        '</label>' +
                    '</div>' +

                    '<div id="passwordBox" ' +
                        (quest.data.password === null ? 'hidden' : '') + '>' +
                        '<label class="form-check-label" for="private">' +
                            'Пароль' +
                        '</label>' +
                        '<input type="text" autocomplete="off" onkeydown="return (event.keyCode!=13);" ' +
                            'class="form-control" ' + 'id="questPassword" value="' +
                                _.escape((quest.data.password !== null ? quest.data.password : '')) +
                                '" placeholder="Пароль">' +
                        '<div class="invalid-feedback">' +
                            'Не используйте пустую строку в качестве пароля.' +
                        '</div>' +
                    '</div>' +
            '</div>'
        );
    }

    static showQuestRedactor(quest) {
        const modal = new bootstrap.Modal(document.getElementById('redactor'));
        const form = document.getElementById('redactorForm');
        console.log(form, modal);
        form.innerHTML = '';
        const buttons = document.getElementById('modalButtons');
        if (buttons !== null) {
            buttons.remove();
        }

        document.getElementById('content').insertAdjacentHTML('beforeend',
            '<div class="modal-footer" id="modalButtons">' +
                '<button type="button" class="btn btn-secondary" style="margin-right: 0.25em" ' +
                    'data-bs-dismiss="modal" id="close">Закрыть</button>' +
                '<button type="button" class="btn btn-primary" id="update">Сохранить</button>' +
            '</div>');
        QuestRedactor.createQuestRedactor(form, quest);

        document.getElementById('private').onchange = () => {
            document.getElementById('passwordBox').hidden = !document.getElementById('passwordBox').hidden;
        };

        document.getElementById('update').onclick = () => {
            let passwordInput = document.getElementById('questPassword');
            let matches = document.getElementById('questDescription').value.match(/#[^\s#]+/g);
            let tags = [];
            if (matches !== null) {
                for (const m of matches) {
                    tags.push(m.slice(1));
                }
            }
            if (document.getElementById('private').checked && passwordInput.value === '') {
                passwordInput.className = 'form-control is-invalid';
                return;
            }
            Quest.updateQuest(JSON.stringify({
                title: document.getElementById('questTitle').value,
                description: document.getElementById('questDescription').value,
                tags: tags,
                password: document.getElementById('private').checked ?
                    document.getElementById('questPassword').value : null,
            }));

            quest.data.title = document.getElementById('questTitle').value;
            quest.data.tags = tags;
            quest.data.description = document.getElementById('questDescription').value;
            quest.data.password = document.getElementById('private').checked ?
                document.getElementById('questPassword').value : null;
            console.log(quest.data.title, quest.data.tags, quest.data.description, quest.data.password);

            modal.hide();
        };

        modal.show();
    }
}
