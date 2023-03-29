import {newInstance} from '@jsplumb/browser-ui';
import {FlowchartConnector} from '@jsplumb/connector-flowchart';
import {Quest} from './quest';
import {Render} from './render';
import {INTERCEPT_BEFORE_DROP, INTERCEPT_BEFORE_START_DETACH} from '@jsplumb/core';
import Panzoom from '@panzoom/panzoom';
import {QuestRedactor} from './blockRedactor';
import {deleteQuestRequest} from './personalCatalog';
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


function createNewBlock(type, text, quest) {
    const lastBlock = {
        //'answer_options': [],
        //'files': [],
        //'hints': [],
        //'movements': [],
        'block_id': undefined,
        'block_text': text,
        'block_type_name': type,
        'pos_x': 0,
        'pos_y': 0,
    };
    if (type == 'open_question' || type == 'choice_question'){
        lastBlock['answers'] = [];
        lastBlock.answers.push({
            'answer_option_id': undefined,
            'next_question_id': undefined,
            'points': 0.0,
            'text': 'Ответ',
        });
        lastBlock['hints'] = [];
    }
    if (type == 'movement'){
        lastBlock['place'] = {
            //'next_question_id': undefined,
                'latitude': 0,
                'longitude': 0,
                //'place_id': undefined,
                'radius': 0,
                //'time_open': 'Sun, 12 Aug 2001 09:00:00 GMT',
                //'time_close': 'Sun, 12 Aug 2001 19:00:00 GMT',
        };
    }
    console.log(lastBlock);
    quest.data.blocks.push(lastBlock);
    return lastBlock;
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


        instance.bind(INTERCEPT_BEFORE_DROP, (params) => {
            const sourceIdSplit = params.sourceId.match(/([a-z]*_?[a-z]*)([0-9]*)/);
            console.log(params)
            if (sourceIdSplit[1] != 'answer_option')
                Quest.connectBlockAndBlock(sourceIdSplit[2], params.connection.target.parentNode.id);
            else {
                const block_id = document.getElementById(params.sourceId).parentElement.parentElement.id;
                Quest.connectAnswerAndBlock(block_id, sourceIdSplit[2], params.connection.target.parentNode.id);
            }
            return true;
        });

        instance.bind(INTERCEPT_BEFORE_START_DETACH, (params) => {
            const sourceIdSplit = params.sourceId.match(/([a-z]*_?[a-z]*)([0-9]*)/);
            if (sourceIdSplit[1] != 'answer_option')
                Quest.disconnectBlockAndBlock(params.connection.sourceId);
            else{
                const block_id = document.getElementById(params.sourceId).parentElement.parentElement.id;
                Quest.disconnectAnswerAndBlock(block_id, sourceIdSplit[2], params.connection.target.parentNode.id);
            } 
        });


        setInterval(() => {
            for (const questBlock of quest.data.blocks) {
                const blok = document.getElementById(questBlock.block_id);
                Quest.updateBlock(blok.id, JSON.stringify({
                    pos_x: parseInt(blok.style.left),
                    pos_y: parseInt(blok.style.top),
                }));
            }
        }, 20000);
        Render.render(quest, instance, sourceEndpoint, targetEndpoint, panzoom);

        document.getElementById('addMBtn').onclick = () => {
            const block = createNewBlock('movement', 'Новое перемещение', quest);
            Quest.addBlock(block).then((result) =>{
                console.log(block);
                Quest.addPlace(block).then((data)=>{
                    console.log(data);
                    Render.renderMovement(quest, block, instance, sourceEndpoint, targetEndpoint);
                });
            });
        };
        document.getElementById('addQBtn').onclick = () => {
            const question = createNewBlock('open_question', 'Новый открытый вопрос', quest);
            Quest.addBlock(question).then((data)=>{
                Quest.addBlockEntity('answer_option', question.block_id, JSON.stringify({
                    points: 0.0,
                    text: 'Ответ',
                })).then((rez) => {
                    console.log('Add new answer'+rez);
                    question.answers[0].answer_option_id =
                        JSON.parse(rez).answer_option_id;
                    console.log('Render question:');
                    Render.renderQuestion(quest, question, 'Открытый вопрос', instance,
                        sourceEndpoint, targetEndpoint);
                });
            });
        };

        document.getElementById('save').onclick = () =>{
            Quest.save(quest.data.quest_id).then(() => document.location = '/profile');
        };
        document.getElementById('addQCBtn').onclick = () => {
            const question = createNewBlock('choice_question', 'Новый вопрос с выбором ответа', quest);
            Quest.addBlock(question).then((data)=>{
                Quest.addBlockEntity('answer_option', question.block_id, JSON.stringify({
                    points: 0.0,
                    text: 'Ответ',
                })).then((rez) => {
                    question.answers[0].answer_option_id =
                        JSON.parse(rez).answer_option_id;
                    Render.renderQuestion(quest, question, 'Вопрос с выбором ответа',
                        instance, sourceEndpoint, targetEndpoint);
                });
            });
        };
        
        document.getElementById('finishBtn').onclick = () => {
            const block = createNewBlock('end_block', '', quest);
            Quest.addBlock(block).then((data) => {
                Render.renderFinish(quest, block, instance, targetEndpoint);
            });
         };

        document.getElementById('redactorQuest').onclick = () => {
            QuestRedactor.showQuestRedactor(quest);
        };

        document.getElementById('deleteQuest').onclick = () => {
            if (confirm('Вы уверены, что хотите удалить квест? Отменить это действие будет невозможно.')){
                console.log(quest);
                deleteQuestRequest(quest.data.quest_id).then(() =>
                    document.location.href = '../profile');
            }
        };
    });
};
