import {Quest} from './quest';
import * as bootstrap from 'bootstrap';

export class BlockRedactor {
    static addTextRedactor(form, label, text) {
        form.innerHTML +=
            '<label for="formControlTextarea" class="form-label">' + label + '</label>' +
            '<textarea class="form-control" id="formControlTextarea" rows="3">' +
            text +
            '</textarea>';
    }

    static addAnswerForOpenQuestion(form, answer) {
        form.innerHTML +=
            '<div class=\'col-8\'>'+
                '<input type="text" class="form-control" id="answerText' + answer.answer_option_id + '"' +
                ' value=' + answer.text + '>' +
            '</div>' +
            '<div class="col-3">' +
                '<div class="input-group">' +
                    '<span class="input-group-text"> Очки </span>' +
                    '<input type="text" class="form-control" id="answerPoints'+ answer.answer_option_id + '"' +
                    ' value=' + answer.points + '>' +
                '</div>' +
            '</div>' +
            '<div class="col-1">' +
                '<button class="btn btn-danger">-</button>' +
            '</div>';
    }

    static addMovementForMovementBlock(form, question) {
        form.innerHTML +=
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
            '</div>'+
            '<div class="col-8">' +
                '<div class=\'input-group\'>' +
                    '<span class="input-group-text"> Очки </span>' +
                    '<input type="text" class="form-control" id="movePoints"  ' +
                        'value=' + question.answer_options[0].points + '>' +
                '</div>' +
            '</div>';
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

    static createOpenQuestionRedactor(form, question) {
        this.addTextRedactor(form, 'Вопрос', question.text);
        form.innerHTML += '<hr><label for="formControlTextarea" class="form-label">Ответы:</label>';
        for (const answer of question.answer_options) {
            this.addAnswerForOpenQuestion(form, answer);
        }
        form.innerHTML +=
            '<div class=\'col-auto\'><button type=\'button\' class=\'btn btn-primary\' id=\'addAnswer\'>' +
                'Добавить ответ' +
            '</button></div>';
        document.getElementById('addAnswer').onclick = () => {
            // TODO add function
        };
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            for (const answer of question.answer_options) {
                const answerId = answer.answer_option_id;
                answer.text = document.getElementById('answerText' + answerId).value;
                answer.points = document.getElementById('answerPoints' + answerId).value;

                document.getElementById('answer_option' + answerId).innerText =
                    document.getElementById('answerText' + answerId).value;
                Quest.updateAnswer(answerId, JSON.stringify({
                    points: answer.points,
                    text: answer.text,
                })).then((response) => console.log(response));
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

    static showRedactor(question) {
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
            BlockRedactor.createOpenQuestionRedactor(form, question);
            break;
        case 'movement':
            BlockRedactor.createMovementRedactor(form, question);
            break;
        case 'choice':
            // TODO: change this to function for "choice"
            BlockRedactor.createOpenQuestionRedactor(form, question);
            break;
        default:
            break;
        }
        modal.show();
    }
}
