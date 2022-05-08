import {newInstance} from '@jsplumb/browser-ui';
import {FlowchartConnector} from '@jsplumb/connector-flowchart';
import {Quest} from './quest';
import {Render} from './render';
import {EVENT_CONNECTION_DETACHED, EVENT_CONNECTION} from '@jsplumb/core';
import Panzoom from '@panzoom/panzoom';
import {QuestRedactor} from './blockRedactor';

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


function load(name, id) {
    if (name === 'new') {
        return Quest.makeNewQuest().then((response) => {
            document.location = 'constructor.html?name=quest&id=' + response.quest_id;
            return;
        });
    } else {
        return Quest.loadQuest(id);
    }
}
function createNewBlock(type, text, quest){
    let lastQuestion = {
        'answer_options': [],
        'files': [],
        'hints': [],
        'movements': [],
        'question_id': undefined,
        'text': text,
        'type': type,
        'pos_x': 0,
        'pos_y': 0,
    }
    if (type!=='movement') {
        lastQuestion.answer_options.push({
            'answer_option_id': undefined,
            'next_question_id': undefined,
            'points': 0.0,
            'text': 'Ответ',
        });
    } else {
        lastQuestion.movements.push( {
            'movement_id': undefined,
            'next_question_id': undefined,
            'place': {
                'coords': [0.0, 0.0],
                'place_id': undefined,
                'radius': 0.0,
                'time_close': 'Sun, 12 Aug 2001 19:00:00 GMT',
                'time_open': 'Sun, 12 Aug 2001 09:00:00 GMT',
            },
        });
    }
    quest.data.questions.push(lastQuestion);
    return lastQuestion;
}
window.onload = () => {
    const query = window.location.href.split('?')[1];
    const queryParams = query.split('&');
    load(queryParams[0].split('=')[1], queryParams[1].split('=')[1]).then((quest) => {
        /* document.getElementById("save").onclick = () => {
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
            Quest.connect(sourceIdSplit[1], 'question', sourceIdSplit[2], connection.target.parentNode.id).then(() =>
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
                Quest.updateEntity('question', blok.id, JSON.stringify({
                    pos_x: parseInt(blok.style.left),
                    pos_y: parseInt(blok.style.top),
                }));
            }
        }, 20000);

        Render.render(quest, instance, sourceEndpoint, targetEndpoint, panzoom);

        document.getElementById('addMBtn').onclick = () => {
            const question = createNewBlock('movement', 'Новое перемещение', quest);
            Quest.addQuestion(quest, question).then((result) =>{
                Quest.addMovement(quest, question).then((data)=>{
                    const place = {
                        coords: [0.0, 0.0],
                        radius: 0.0,
                    };
                    Quest.addNewPlace(quest, JSON.stringify(place), question).then((rez)=>{
                        Quest.connect('question', 'movement',
                        question.question_id,
                        question.movements[0].movement_id);
                        Quest.connect('movement', 'place',
                        question.movements[0].movement_id,
                        question.movements[0].place.place_id);
                        Render.renderMovement(quest, question, instance, sourceEndpoint,
                            targetEndpoint);
                    });
                });
            });
        };

        document.getElementById('addQBtn').onclick = () => {
            const question = createNewBlock('open', 'Новый открытый вопрос', quest);
            Quest.addQuestion(quest, question).then((data)=>{
                Quest.addEntity('answer_option', JSON.stringify({
                    points: 0.0,
                    text: 'Ответ',
                })).then((rez) => {
                    console.log('Add new answer'+rez);
                    question.answer_options[0].answer_option_id =
                        JSON.parse(rez).answer_option_id;
                    console.log('Render question:');
                    Quest.connect('question', 'answer_option',
                    question.question_id,
                    question.answer_options[0].answer_option_id);
                    Render.renderQuestion(question, 'Открытый вопрос', instance,
                        sourceEndpoint, targetEndpoint);
                });
            });
        };

        document.getElementById('save').onclick = () =>{
            console.log("Saving quest ", quest);
            Quest.save(quest.data.quest_id);
        }
        document.getElementById('addQCBtn').onclick = () => {
            const question = createNewBlock('choice', 'Новый вопрос с выбором ответа', quest);
            Quest.addQuestion(quest, questionInd).then((data)=>{
                Quest.addEntity('answer_option', JSON.stringify({
                    points: 0.0,
                    text: 'Ответ',
                })).then((rez) => {
                    question.answer_options[0].answer_option_id =
                        JSON.parse(rez).answer_option_id;
                    Quest.connect('question', 'answer_option',
                        question.question_id,
                        question.answer_options[0].answer_option_id);
                    Render.renderQuestion(quest, question, 'Вопрос с выбором ответа',
                        instance, sourceEndpoint, targetEndpoint);
                });
            });
        };
        document.getElementById('redactorQuest').onclick = () => {
            QuestRedactor.showQuestRedactor(quest);
        };
    });
};
