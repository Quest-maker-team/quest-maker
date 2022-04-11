import { newInstance } from "@jsplumb/browser-ui";
import { FlowchartConnector } from "@jsplumb/connector-flowchart";
import {Quest} from "./quest";
import { Render } from "./render";
import { EVENT_CONNECTION_DETACHED, EVENT_CONNECTION } from "@jsplumb/core";

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

Quest.loadQuest(2).then(newQuest =>{
    let quest = newQuest;
    Render.render(quest, instance, sourceEndpoint, targetEndpoint);
    /*document.getElementById("save").onclick = () => {
        quest.save().then(() => console.log("save"));
    }*/
    return quest;
}).then(quest => {
    instance.bind(EVENT_CONNECTION, (connection) => {
        console.log("connect");
        console.log(connection);
        let source = connection.source;
        let target = connection.target;
        let typeTarget = "question";
        let typeSource;
        let sourceId = source.id;
        if (source.id.includes("answer")) {
            console.log("answer");
            typeSource = "answer_options";
            sourceId = source.id.slice("answer".length);
        }
        else {
            console.log(quest.data.questions.find(question => question.question_id == sourceId));
            typeSource = quest.data.questions.find(question => question.question_id == sourceId).type;
            if (typeSource === "movement")
                typeSource = "place";
            else
                typeSource = "question";
        }
        Quest.connect(typeSource, typeTarget, sourceId, target.id).then(() => console.log("success"));
    });
    instance.bind(EVENT_CONNECTION_DETACHED, (connection) => {
        console.log("disconnect");
        console.log(connection);
    });

});

export function createNewBlock(type, text, renderFunction){
    console.log(text);
    let max = quest.data.questions.reduce((acc, curr) => acc.question_id > curr.question_id ? acc : curr);
    let newBlockId = max.question_id + 1;
    console.log(newBlockId);
    quest.data.questions.push( {
        "answer_options": [
            {
                "answer_option_id": undefined,
                "next_question_id": undefined,
                "points": 0.0,
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
   renderFunction(quest, quest.data.questions.slice(-1)[0], instance, sourceEndpoint, targetEndpoint, "absolute");
   return newBlockId;
}
 document.getElementById("addMBtn").onclick = () => {
    let movements = quest.data.questions.filter(item => item.type == "movement");
    console.log(movements);
    let maxMovement = movements.reduce((acc, curr) =>
    acc.movements[0].movement_id >= curr.movements[0].movement_id  ? acc : curr);
    console.log(maxMovement == undefined);
    let maxId = (maxMovement != undefined ? maxMovement.movements[0].movement_id+1 : 1);
    console.log(maxId);
    let questionId = createNewBlock("movement", "Новое перемещение", Render.renderMovement);
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
    Quest.pushMovement(quest, questionId, maxId);
}

document.getElementById("addQBtn").onclick = () => {
    let questionId =  createNewBlock("open", "Новый открытый вопрос", Render.renderOpenQuestion);
    Quest.pushQuestion(quest, questionId);
}
