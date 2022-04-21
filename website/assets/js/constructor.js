import {newInstance} from '@jsplumb/browser-ui';
import {FlowchartConnector} from '@jsplumb/connector-flowchart';
import {Quest} from './quest';
import {Render} from './render';
import {EVENT_CONNECTION_DETACHED, EVENT_CONNECTION} from '@jsplumb/core';

// load static images
require.context(
    '../', // context folder
    true, // include subdirectories
    /\.(svg|png|jpe?g|gif|ico)(\?.*)?$/i, // RegExp
);

const containerElement = document.getElementById('container');

const instance = newInstance({
    container: containerElement,
});

const sourceEndpoint = {
    endpoint: {type: 'Dot', options: {radius: 5}},
    connector: {type: 'Flowchart', options: {cornerRadius: 2}},
    source: true,
};

const targetEndpoint = {
    endpoint: {type: 'Rectangle'},
    // paintStyle: { fill: "green" },
    maxConnections: -1,
    source: false,
    target: true,
    connectionsDetachable: true,
    anchor: [0.5, 0, 0, -1],
};

Quest.loadQuest(2).then((newQuest) => {
    const quest = newQuest;
    Render.render(quest, instance, sourceEndpoint, targetEndpoint);
    return quest;
}).then((quest) => {
    /* document.getElementById("save").onclick = () => {
        quest.save().then(() => console.log("save"));
    }*/

    instance.bind(EVENT_CONNECTION, (connection) => {
        let sourceIdSplit = connection.source.id.match(/([a-z]*_?[a-z]*)([0-9]*)/);
        Quest.connect(sourceIdSplit[1], 'question', sourceIdSplit[2], connection.target.id).then(() =>
            console.log('connect success'));
    });

    instance.bind(EVENT_CONNECTION_DETACHED, (connection) => {
        let sourceIdSplit = connection.source.id.match(/([a-z]*_?[a-z]*)([0-9]*)/);
        Quest.disconnect(sourceIdSplit[1], 'question', sourceIdSplit[2]).then(() =>
            console.log('disconnect success'));
    });
    return quest;
}).then((quest) => {
    const createNewBlock = function(type, text, renderFunction) {
        console.log(text);
        const max = quest.data.questions.reduce((acc, curr) => acc.question_id > curr.question_id ? acc : curr);
        const newBlockId = max.question_id + 1;
        console.log(newBlockId);
        quest.data.questions.push( {
            'answer_options': [
                {
                    'answer_option_id': undefined,
                    'next_question_id': undefined,
                    'points': 0.0,
                    'text': 'Ответ',
                },
            ],
            'files': [],
            'hints': [],
            'movements': [],
            'question_id': newBlockId,
            'text': text,
            'type': type,
        });
        console.log(quest.data.questions.slice(-1)[0]);
        renderFunction(quest, quest.data.questions.slice(-1)[0], instance, sourceEndpoint, targetEndpoint, 'absolute');
        return newBlockId;
    };

    document.getElementById('addMBtn').onclick = () => {
        const movements = quest.data.questions.filter((item) => item.type == 'movement');
        console.log(movements);
        const maxMovement = movements.reduce((acc, curr) =>
            acc.movements[0].movement_id >= curr.movements[0].movement_id ? acc : curr);
        console.log(maxMovement == undefined);
        const maxId = (maxMovement != undefined ? maxMovement.movements[0].movement_id+1 : 1);
        console.log(maxId);
        const questionId = createNewBlock('movement', 'Новое перемещение', Render.renderMovement);
        console.log(quest.data.questions);
        quest.data.questions.slice(-1)[0].movements.push({
            'movement_id': maxId,
            'next_question_id': undefined,
            'place': {
                'coords': '(0.0,0.0)',
                'place_id': undefined,
                'radius': 0,
                'time_close': 'Sun, 12 Aug 2001 19:00:00 GMT',
                'time_open': 'Sun, 12 Aug 2001 09:00:00 GMT',
            },
        });
        Quest.pushMovement(quest, questionId, maxId);
    };

    document.getElementById('addQBtn').onclick = () => {
        const questionId = createNewBlock('open', 'Новый открытый вопрос', Render.renderOpenQuestion);
        Quest.pushQuestion(quest, questionId);
    };
});
