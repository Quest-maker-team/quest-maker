import {newInstance} from '@jsplumb/browser-ui';
import {FlowchartConnector} from '@jsplumb/connector-flowchart';
import {Quest} from './quest';
import {Render} from './render';
import {EVENT_CONNECTION_DETACHED, EVENT_CONNECTION} from '@jsplumb/core';
import Panzoom from '@panzoom/panzoom';

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


Quest.loadQuest(1, 24).then(quest => {
    /*document.getElementById("save").onclick = () => {
        Quest.save(24).then(() => console.log("save"));
    }*/

    // panzoom init
    const panzoom = Panzoom(containerElement, {
        canvas: true,
        maxScale: 5,
        cursor: 'default',
    });

    // Panning and pinch zooming are bound automatically (unless disablePan is true).
    // There are several available methods for zooming
    // that can be bound on button clicks or mousewheel.
    // button.addEventListener('click', panzoom.zoomIn);
    containerElement.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

    containerElement.addEventListener('newEndpointCreating', (event) => {
        panzoom.getOptions().exclude.push(event.detail.endpointElem);
    });

    containerElement.addEventListener('panzoomzoom', (event) => {
        instance.setZoom(event.detail.scale);
    });

    containerElement.addEventListener('panzoomstart', (event) => {
        containerElement.parentElement.style.cursor = 'move';
    });

    containerElement.addEventListener('panzoomend', (event) => {
        containerElement.parentElement.style.cursor = 'default';
    });


    instance.bind(EVENT_CONNECTION, (connection) => {
        const sourceIdSplit = connection.source.id.match(/([a-z]*_?[a-z]*)([0-9]*)/);
        Quest.connect(sourceIdSplit[1], 'question', sourceIdSplit[2], connection.target.id).then(() =>
            console.log('connect success'));
    });

    instance.bind(EVENT_CONNECTION_DETACHED, (connection) => {
        const sourceIdSplit = connection.source.id.match(/([a-z]*_?[a-z]*)([0-9]*)/);
        Quest.disconnect(sourceIdSplit[1], 'question', sourceIdSplit[2]).then(() =>
            console.log('disconnect success'));
    });

    setInterval(() => {
        for (const question of quest.data.questions) {
            const blok = document.getElementById(question.question_id);
            Quest.updateQuestion(blok.id, JSON.stringify({
                pos_x: parseInt(blok.style.left),
                pos_y: parseInt(blok.style.top),
            }));
        }
    }, 20000);

    Render.render(quest, instance, sourceEndpoint, targetEndpoint, panzoom);

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