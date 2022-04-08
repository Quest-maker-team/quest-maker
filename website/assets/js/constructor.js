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

let quest = new Quest(TestJSON);

 document.getElementById("addMBtn").onclick = function () {
    let max = quest.data.questions.reduce((acc, curr) => acc.question_id > curr.question_id ? acc : curr);
    let newBlockId = max.question_id+1;
    console.log(newBlockId);
    quest.data.questions.push( {
       "answer_options": [],
       "files": [],
       "hints": [],
       "movements": [],
       "question_id": newBlockId,
       "text": "Новое передвижение № " + newBlockId.toString(),
       "type": "movement"
   });
   console.log(quest.data.questions[newBlockId-1]);
   Render.RenderNewBlock(quest, quest.data.questions[newBlockId-1],instance,sourceEndpoint,targetEndpoint,"Movement");
}

document.getElementById("addQBtn").onclick = function () {
    let max = quest.data.questions.reduce((acc, curr) => acc.question_id > curr.question_id ? acc : curr);
    let newBlockId = max.question_id+1;
    console.log(newBlockId);
    quest.data.questions.push( {
       "answer_options": [],
       "files": [],
       "hints": [],
       "movements": [],
       "question_id": newBlockId,
       "text": "Новый открытый вопрос № " + newBlockId.toString(),
       "type": "open"
   });
   console.log(quest.data.questions[newBlockId-1]);
   Render.RenderNewBlock(quest,quest.data.questions[newBlockId-1],instance,sourceEndpoint,targetEndpoint,"Open");
}

Render.Render(quest,instance, sourceEndpoint, targetEndpoint);