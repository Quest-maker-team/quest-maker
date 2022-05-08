import {newInstance} from '@jsplumb/browser-ui';
import {Render} from './render';

export class Quest {
    constructor(data) {
        this.data = data;
        console.log("Created quest", data);
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
                        // console.log(xmlhttp.responseText);
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
        return Quest.makeRequest('GET', 'api/constructor/quest/' + id).then((data) => {
            return new Quest(JSON.parse(data));
        });
    }

    static makeNewQuest() {
        return Quest.makeRequest('POST', 'api/constructor/quest', JSON.stringify({
            title: '',
            hidden: true,
        })).then((response) => {
            return JSON.parse(response);
        });
    }

    static addEntity(type, data) {
        const url = 'api/constructor/' + type;
        return Quest.makeRequest('POST', url, data);
    }

    static updateEntity(type, id, data) {
        const url = 'api/constructor/' + type + '/' + id;
        return Quest.makeRequest('PUT', url, data);
    }

    static connect(type1, type2, id1, id2) {
        const url = 'api/constructor/' + type1 + '/' + id1 + '/' + type2 + '/' + id2;
        return Quest.makeRequest('PUT', url);
    }

    static disconnect(type1, type2, id1) {
        const url = 'api/constructor/' + type1 + '/' + id1 + '/' + type2;
        return Quest.makeRequest('DELETE', url);
    }

    static deleteEntity(type, id) {
        const url = 'api/constructor/' + type + '/' + id;
        return Quest.makeRequest('DELETE', url);
    }


    static save(id) {
        const url = 'api/constructor/save/' + id;
        return Quest.makeRequest('POST', url);
    }

    static addNewPlace(place, question) {
        const url = 'api/constructor/place';
        return Quest.makeRequest('POST', url, place).then((result) => {
            console.log('success add new place '+ result);
            const id = JSON.parse(result).place_id;
            question.movements[0].place.place_id = id;
            console.log('id = '+ id);
            return id;
        });
    }

    static addQuestion(question) {
        return Quest.makeRequest('POST', 'api/constructor/question', JSON.stringify({
            type: question.type,
            text: ' ',
            pos_x: 0,
            pos_y: 0,
        })).then((result) => {
            console.log('success add new question '+ result);
            const id = JSON.parse(result).question_id;
            question.question_id = id;
            console.log('id = '+ id);
            return id;
        }, (error) => {
            console.log('failed add new question');
        });
    }

    static addMovement(move) {
        return Quest.makeRequest('POST', 'api/constructor/movement', JSON.stringify({})).then((result) => {
            console.log('success add new movement ' + result);
            const id = JSON.parse(result).movement_id;
            move.movements[0].movement_id = id;
            console.log('id = ' + id);
            return id;
        }, (error) => {
            console.log('failed add new movement');
        });
    }
}
