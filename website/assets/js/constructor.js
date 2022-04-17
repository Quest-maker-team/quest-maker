import { newInstance } from "@jsplumb/browser-ui";
import { FlowchartConnector } from "@jsplumb/connector-flowchart";
//import { Render } from "./render"
import {Quest} from "./quest";
import { Render } from "./render";

// load static images
require.context(
    '../', // context folder
    true, // include subdirectories
    /\.(svg|png|jpe?g|gif|ico)(\?.*)?$/i, // RegExp
);

let containerElement = document.getElementById("container");

let instance = newInstance({
    container: containerElement,
});

let sourceEndpoint = {
    endpoint: { type: "Dot", options: { radius: 5 } },
    connector: { type: "Flowchart", options: { cornerRadius: 2 } },
    source: true,
};

let targetEndpoint = {
    endpoint: { type: "Rectangle" },
    //paintStyle: { fill: "green" },
    maxConnections: -1,
    source: false,
    target: true,
    connectionsDetachable: true,
    anchor: [ 0.5, 0, 0, -1 ],
};

Quest.loadQuest(1).then(newQuest =>{
    let quest = newQuest;
    Render.render(quest, instance, sourceEndpoint, targetEndpoint);
    return quest;
});

/*export function createNewBlock(type, text, renderFunction){
    console.log(text);
    let max = quest.data.questions.reduce((acc, curr) => acc.question_id > curr.question_id ? acc : curr);
    let newBlockId = max.question_id + 1;
    console.log(newBlockId);
    quest.data.questions.push( {
        "answer_options": [
            {
                "next_question_id": undefined,
                "points": 0,
                "text": "Ответ"
            }
        ],
       "files": [],
       "hints": [],
       "movements": [],
       "question_id": newBlockId,
       "text": text,
       "type": type
   });
   console.log(quest.data.questions.slice(-1)[0]);
   renderFunction(quest, quest.data.questions.slice(-1)[0], instance, sourceEndpoint, targetEndpoint);
   return quest.data.questions.slice(-1)[0];
}
 document.getElementById("addMBtn").onclick = () => {
    let movements = quest.data.questions.filter(item => item.type == "movement");
    console.log(movements);
    let maxMovement = movements.reduce((acc, curr) =>
    acc.movements[0].movement_id >= curr.movements[0].movement_id  ? acc : curr);
    console.log(maxMovement == undefined);
    let maxId = (maxMovement != undefined ? maxMovement.movements[0].movement_id+1 : 1);
    console.log(maxId);
    createNewBlock("movement", "Новое перемещение", Render.renderMovement);
    console.log(quest.data.questions);
    quest.data.questions.slice(-1)[0].movements.push({
        "movement_id": maxId,
        "next_question_id": undefined,
        "place": {
            "coords": "(0.0,0.0)",
            "place_id": undefined,
            "radius": 0,
            "time_close": "Sun, 12 Aug 2001 19:00:00 GMT",
            "time_open": "Sun, 12 Aug 2001 09:00:00 GMT"
        }
    });
}

document.getElementById("addQBtn").onclick = () => {
    createNewBlock("open", "Новый открытый вопрос", Render.renderOpenQuestion);
}
*/