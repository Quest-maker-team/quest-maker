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
                        // console.log("fail to load");
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

    static makePostRequest(url, data) {
        return new Promise(function(resolve, reject) {
            const xmlhttp = new XMLHttpRequest();
            xmlhttp.open('POST', url);
            xmlhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        resolve(xmlhttp.response);
                    } else {
                        // console.log("fail to load");
                        reject(xmlhttp.status);
                    }
                }
            };

            if (data !== undefined) {
                xmlhttp.send(JSON.stringify(data));
            } else {
                xmlhttp.send();
            }
            // console.log("POST: " + json);
        });
    }

    static loadQuest(id) {
        const url = '/api/db/quest/' + id.toString();
        return Quest.makeRequest('GET', url).then((data) => {
            console.log('success');
            return new Quest(JSON.parse(data));
        });
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

    static disconnect(type1, type2, id1, id2) {
        const url = 'api/' + type1 + '/' + id1 + '/' + type2 + '/' + id2;
        return Quest.makeRequest('DELETE', url);
    }

    save() {
        const url = 'api/save/' + this.data.quest_id;
        return Quest.makePostRequest(url);
    }

    static pushQuestion(quest, id) {
        const url = '/api/';
        const questionToSend = quest.data.questions.find((question) => question.question_id===id);

        new Promise((resolve, reject) => {
            resolve(Quest.makePostRequest(url+'question', {'type': questionToSend.type, 'text': questionToSend.text}).then((data) => {
                console.log(data);
                console.log(id === data['question_id']);
                quest.data.questions.find((question) => question.question_id===id).question_id = data['question_id'];
                id = data['question_id'];
            }).then((data)=>{
                for (let i = 0; i < questionToSend.answer_options.length; i++) {
                    new Promise((resolve, reject) => {
                        resolve(Quest.makePostRequest(url+'answer_option', {'text': questionToSend.answer_options[i].text, 'points': questionToSend.answer_options[i].points}).then((data) => {
                            console.log(data);
                            quest.data.questions.find((question) => question.question_id===id).answer_options[i].answer_option_id = data['answer_option_id'];
                        }));
                    });
                }
            }));
        });
    }

    static pushMovement(quest, id, moveId) {
        const url = '/api/';
        const questionToSend = quest.data.questions.find((question) => question.question_id===id);
        console.log('A');
        new Promise((resolve, reject) => {
            resolve(Quest.makePostRequest(url+'question', {'type': questionToSend.type, 'text': questionToSend.text}).then((data) => {
                console.log('AA');
                console.log(data);
                console.log(id === data['question_id']);
                quest.data.questions.find((question) => question.question_id===id).question_id = data['question_id'];
                id = data['question_id'];
            }).then((dataM) =>{
                console.log(dataM);
                new Promise((resolve, reject) => {
                    resolve(Quest.makePostRequest(url+'movement', {})).then((dataMM) => {
                        console.log(dataMM);
                    });
                });
            })
            );
        });
    }
}
