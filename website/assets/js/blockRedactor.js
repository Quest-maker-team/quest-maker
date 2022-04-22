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

    static deleteAnswer(answer, question, instance) {
        if (confirm('Вы действительно хотите удалить вариант ответа? Отменить действие будет не возможно.')) {
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
        }
    }

    static addAnswerForQuestion(element_id, answer, question, instance) {
        document.getElementById(element_id).insertAdjacentHTML('beforeend',
            '<div class="row pb-1" id="ansblock' + answer.answer_option_id + '">' +
                '<div class="col-7">'+
                    '<input type="text" onkeydown="return (event.keyCode!=13);" class="form-control" id="answerText' +
                        answer.answer_option_id + '" value="' + answer.text + '">' +
                '</div>' +
                '<div class="col-4">' +
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
            this.deleteAnswer(answer, question, instance);
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

    static createOpenQuestionRedactor(form, question, instance, sourceEndpoint) {
        this.addTextRedactor(form, 'Вопрос', question.text);
        form.insertAdjacentHTML('beforeend', 
            '<hr><label for="formControlTextarea" class="form-label">Ответы:</label>');
        form.insertAdjacentHTML('beforeend', '<div id="OQanswers"></div>');
        form.insertAdjacentHTML('beforeend',
            '<div class="col-auto"><button type="button" class="btn btn-primary" id="addAnswer">' +
                'Добавить ответ' +
            '</button></div>'
        );
        for (const answer of question.answer_options) {
            this.addAnswerForQuestion('OQanswers', answer, question, instance);
        }

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
            });
        };
        document.getElementById('update').onclick = () => {
            question.text = document.getElementById('formControlTextarea').value;
            document.getElementById(question.question_id).getElementsByClassName('card-text')[0].textContent =
                question.text;
            for (const answer of question.answer_options) {
                const answerId = answer.answer_option_id;
                answer.text = document.getElementById('answerText' + answerId).value;
                answer.points = document.getElementById('answerPoints' + answerId).value;
                question.text = document.getElementById('formControlTextarea').value;
                let answerTable = document.getElementById('anstab' + question.question_id);

                document.getElementById('answer_option' + answerId).innerText =
                    document.getElementById('answerText' + answerId).value;
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
            BlockRedactor.createOpenQuestionRedactor(form, question, instance, sourceEndpoint);
            break;
        case 'movement':
            BlockRedactor.createMovementRedactor(form, question);
            break;
        case 'choice':
            // TODO: change this to function for "choice"
            BlockRedactor.createOpenQuestionRedactor(form, question, instance, sourceEndpoint);
            break;
        default:
            break;
        }
        modal.show();
    }
}
