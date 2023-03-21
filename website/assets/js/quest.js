import {newInstance} from '@jsplumb/browser-ui';
import {Render} from './render';

export class Quest {
    constructor(data) {
        this.data = data;
        console.log('Created quest', data);
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

    static addBlockEntity(type, block_id, data) {
        const url = 'api/constructor/' + type + '/block/' + block_id;
        return Quest.makeRequest('POST', url, data);
    }

    static updateBlock(id, data){
        const url = 'api/constructor/block/' + id;
        return Quest.makeRequest('PUT', url, data);
    }

    static updateQuest(data){
        const url = 'api/constructor/quest';
        return Quest.makeRequest('PUT', url, data);
    }

    static updateEntity(type, id, block_id, data) {
        const url = 'api/constructor/block/' + block_id + '/' + type + '/' + id;
        return Quest.makeRequest('PUT', url, data);
    }

    static connectBlockAndBlock(sourceId, targetId) {
        const url = 'api/constructor/source_block/' + sourceId + '/target_block/' + targetId;
        return Quest.makeRequest('PUT', url);
    }

    static connectAnswerAndBlock(hostId, answerId, blockId) {
        const url = 'api/constructor/answer_host/' + hostId + '/answer_id/' + answerId + '/block/' + blockId
        return Quest.makeRequest('PUT', url);
    }

    static disconnectBlockAndBlock(sourceId) {
        const url = 'api/constructor/source_block/' + sourceId;
        return Quest.makeRequest('PUT', url);
    }

    static disconnectAnswerAndBlock(hostId, answerId) {
        const url = 'api/constructor/answer_host/' + hostId + '/answer_id/' + answerId
        return Quest.makeRequest('PUT', url);
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

    static addBlock(questBlock) {
        return Quest.makeRequest('POST', 'api/constructor/block', JSON.stringify({
            block_type_name: questBlock.block_type_name,
            text: '',
            pos_x: questBlock.pos_x,
            pos_y: questBlock.pos_y,
        })).then((result) => {
            console.log('success add new block '+ result);
            const id = JSON.parse(result).block_id;
            questBlock.block_id = id;
            console.log('id = '+ id);
            return id;
        }, (error) => {
            console.log('failed add new block');
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
