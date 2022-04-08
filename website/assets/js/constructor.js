import { newInstance } from "@jsplumb/browser-ui";
import { FlowchartConnector } from "@jsplumb/connector-flowchart";
//import { Render } from "./render"
import {Quest} from "./quest";
import { Render } from "./render";
import {TestJSON} from "./testJSON";

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

export function createNewBlock(type, text, renderFunction){
    console.log(text);
    let max = quest.data.questions.reduce((acc, curr) => acc.question_id > curr.question_id ? acc : curr);
    let newBlockId = max.question_id + 1;
    console.log(newBlockId);
    quest.data.questions.push( {
       "answer_options": [],
       "files": [],
       "hints": [],
       "movements": [],
       "question_id": newBlockId,
       "text": text,
       "type": type
   });
   console.log(quest.data.questions.slice(-1)[0]);
   renderFunction(quest, quest.data.questions.slice(-1)[0], instance, sourceEndpoint, targetEndpoint);
}

let quest = new Quest(TestJSON);

 document.getElementById("addMBtn").onclick = function () {
    createNewBlock("movement", "Новое перемещение", Render.renderMovement);
}

document.getElementById("addQBtn").onclick = function () {
    createNewBlock("open", "Новый открытый вопрос", Render.renderOpenQuestion);
}

Render.Render(quest, instance, sourceEndpoint, targetEndpoint);