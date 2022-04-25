import {newInstance} from '@jsplumb/browser-ui';
import {Render} from './render';


export class Quest {
    constructor(data) {
        this.data = data;
    }

    static makeRequest(method, url, data) {
        return new Promise(function(resolve, reject) {
            const xmlhttp = new XMLHttpRequest();
            xmlhttp.open(method, url);
            xmlhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        resolve(xmlhttp.response);
                    } else {
                        console.log(xmlhttp.responseText);
                        reject(xmlhttp.status);
                    }
                }
            };

            if (data !== undefined) {
                xmlhttp.send(data);
            } else {
                xmlhttp.send();
            }
        });
    }

    static loadQuest(id) {
        return Quest.makeRequest('GET', 'api/db/quest/' + id.toString()).then(data => {
            return new Quest(JSON.parse(data));
        });
    }

    static loadDraft(id) {
        return Quest.makeRequest('GET', 'api/draft/quest/' + id.toString()).then(data => {
            return new Quest(JSON.parse(data));
        });
    }

    static makeNewQuest() {
        return Quest.makeRequest('POST', 'api/quest', JSON.stringify({
            title: '',
            hidden: true,
        })).then(response => {
            let responseData = JSON.parse(response);
            let data = {
                quest_id: responseData.quest_id,
                start_question_id: responseData.start_question_id,
                title: '',
                description: '',
                password: '',
                questions: [
                    {
                        question_id: responseData.start_question_id,
                        answer_options: [
                            {
                                answer_option_id: responseData.first_answer_id,
                                text: '',
                                points: 0,
                            }
                        ],
                        pos_x: 200,
                        pos_y: 100,
                        text: '',
                        type: 'start',
                    },
                    {
                        question_id: responseData.end_question_id,
                        answer_options: [],
                        pos_x: 400,
                        pos_y: 300,
                        text: '',
                        type: 'end',
                    },
                ]
            };
            Quest.updateQuestion(responseData.start_question_id, JSON.stringify({
                pos_x: 200,
                pos_y: 100,
                text: '',
                type: 'start',
            }));
            Quest.updateAnswer(data.questions[0].answer_options[0].answer_option_id, JSON.stringify({
                text: '',
                points: 0,
            })).then(() => {
                Quest.connect('question', 'answer_option', responseData.start_question_id, data.questions[0].answer_options[0].answer_option_id);
            });
            Quest.updateQuestion(responseData.start_question_id, JSON.stringify({
                pos_x: 400,
                pos_y: 300,
                text: '',
                type: 'end'}));
            return new Quest(data);
        })
    }

    static addAnswer(answer) {
        const url = 'api/answer_option';
        return Quest.makeRequest('POST', url, answer);
    }

    static updateQuest(id, questParams){
        const url = 'api/quest/' + id;
        return Quest.makeRequest('PUT', url, questParams);
    }

    static updateAnswer(id, answer) {
        const url = 'api/answer_option/' + id;
        return Quest.makeRequest('PUT', url, answer);
    }

    static updateQuestion(id, question) {
        const url = 'api/question/' + id;
        return Quest.makeRequest('PUT', url, question);
    }

    static connect(type1, type2, id1, id2) {
        const url = 'api/' + type1 + '/' + id1 + '/' + type2 + '/' + id2;
        return Quest.makeRequest('PUT', url);
    }

    static disconnect(type1, type2, id1) {
        const url = 'api/' + type1 + '/' + id1 + '/' + type2;
        return Quest.makeRequest('DELETE', url);
    }

    static deleteEntity(type, id) {
        const url = 'api/' + type + '/' + id;
        return Quest.makeRequest('DELETE', url);
    }

    static save(draft) {
        const url = 'api/save/' + draft;
        return Quest.makePostRequest(url);
    }

    static addNewPlace(quest, place, questionInd){
        const url = 'api/place';
        return Quest.makeRequest('POST', url, place).then(result=>{
            console.log('success add new place '+ result);
            const id = JSON.parse(result).place_id;
            quest.data.questions[questionInd].movements[0].place.place_id = id;
            console.log('id = '+ id);
            return id;
        });
    }

    static addQuestion(quest, questionInd) {
        return Quest.makeRequest('POST', 'api/question', JSON.stringify({
            type: quest.data.questions[questionInd].type,
            text: " " ,
            pos_x: 0,
            pos_y: 0
        }))
        .then(result => {
            console.log('success add new question '+ result);
            const id = JSON.parse(result).question_id;
            quest.data.questions[questionInd].question_id = id;
            console.log('id = '+ id);
            return id;
        }, error => {
            console.log('failed add new question');
        });
    
    }

    static addMovement(quest, moveInd) {
        return Quest.makeRequest('POST', 'api/movement', JSON.stringify({}))
        .then(result => {
            console.log('success add new movement '+ result);
            const id = JSON.parse(result).movement_id;
            quest.data.questions[moveInd].movements[0].movement_id = id;
            console.log('id = '+ id);
            return id;
        }, error => {
            console.log('failed add new movement');
        });
    }
}