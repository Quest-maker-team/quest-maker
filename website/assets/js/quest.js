import {newInstance} from "@jsplumb/browser-ui";
//import { Render } from "./render"
import {Render} from "./render";

export class Quest{
    constructor(data) {
       this.data = data;
    }

    static makeLoadRequest(url){
        return new Promise(function (resolve, reject) {
            let xmlhttp = new XMLHttpRequest();

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        resolve(xmlhttp.responseText);
                    } else {
                        reject(xmlhttp.status);
                    }
                }
            };
            xmlhttp.open("GET", url, true);
            xmlhttp.send();
        });
    }
    static makePostRequest(url, json, resolve){
        return new Promise(function (resolve, reject) {
            let xmlhttp = new XMLHttpRequest();
            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        resolve(xmlhttp.response);
                    } else {
                        console.log("fail to load")
                    }
                }
            };
            xmlhttp.open("POST", url);
            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send(JSON.stringify(json));
            console.log("POST: "+JSON.stringify(json));
        });                                             
    }
    static loadQuest(id){
        let url = '/api/db/quest/' + id.toString();

        return new Promise((resolve, reject) => {
            resolve(this.makeLoadRequest(url).then(data => {
                console.log("success");
                return new Quest(JSON.parse(data));
            }));
        });
    }

    showQuest(){
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
            maxConnections: -1,
            source: false,
            target: true,
            connectionsDetachable: true,
            anchor: [ 0.5, 0, 0, -1 ],
        };

        Render.render(this, instance, sourceEndpoint, targetEndpoint);
    }
    static pushQuestion(quest, id){
        let url = '/api/';
        let questionToSend  = quest.data.questions.find(question => question.question_id===id);

        new Promise((resolve, reject) => {
            resolve(Quest.makePostRequest(url+"question", {"type": questionToSend.type, "text":questionToSend.text}).then(data => {
                console.log(data);
                console.log(id === data["question_id"]);
                quest.data.questions.find(question => question.question_id===id).question_id = data["question_id"];
                id = data["question_id"];
            }).then(data=>{
                for(let i = 0; i < questionToSend.answer_options.length; i++){
                    new Promise((resolve, reject) => {
                        resolve(Quest.makePostRequest(url+"answer_option", {"text": questionToSend.answer_options[i].text, "points": questionToSend.answer_options[i].points}).then(data => {
                            console.log(data);
                            quest.data.questions.find(question => question.question_id===id).answer_options[i].answer_option_id = data["answer_option_id"];
                        }));
                    });
                }

            }));
        });    
                
    }
    static pushMovement(quest, id, moveId){
        let url = '/api/';
        let questionToSend  = quest.data.questions.find(question => question.question_id===id);
        console.log("A");
        new Promise((resolve, reject) => {
            resolve(Quest.makePostRequest(url+"question", {"type": questionToSend.type, "text":questionToSend.text}).then(data => {
                console.log("AA");
                console.log(data);
                console.log(id === data["question_id"]);
                quest.data.questions.find(question => question.question_id===id).question_id = data["question_id"];
                id = data["question_id"];
            }).then(dataM =>{
                console.log(dataM);
                new Promise((resolve, reject) => {
                    resolve(Quest.makePostRequest(url+"movement", {})).then(dataMM => {console.log(dataMM);});
                });
            })
             )})
            }
        
    }