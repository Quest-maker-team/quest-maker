import {BlockRedactor} from "./blockRedactor";
import {consume} from "@jsplumb/browser-ui";

export class Render{
    static renderBlockBase(question, width, title, position){
        let block = document.createElement("div");
        block.id = question.question_id;
        block.className = "position-absolute border-2 card";
        block.style.width = width;
        block.style.top = position[0];
        block.style.left = position[1];

        let blockBody = document.createElement("div");
        blockBody.className = "card-body";
        blockBody.innerHTML = "<h5 class=\"card-title text-center\">" + title + "</h5>" +
                                "<hr>" +
                                "<p class=\"card-text text-center text-truncate\">" + question.text + "</p>";
        block.append(blockBody);

        block.ondblclick = () => {
            BlockRedactor.showRedactor(question);
        }

        document.getElementById("container").append(block);
        return block;
    }

    static addDeleteButton(quest, block, instance, answerElements){
        let deleteButton = document.createElement("button");
        deleteButton.id = "btn" + block.id;
        deleteButton.className = "btn-close btn-danger";
        deleteButton.style.position = "absolute";
        deleteButton.style.top = "0";
        deleteButton.style.right = "0";
        deleteButton.onclick = () => {
            if (answerElements !== undefined) {
                for (let answerElement of answerElements) {
                    instance.deleteConnectionsForElement(answerElement);
                    instance.selectEndpoints({element: answerElement}).deleteAll();
                    delete instance.getManagedElements()[answerElement.id];
                }
            }
            instance.deleteConnectionsForElement(block);

            instance.selectEndpoints({element: block}).deleteAll();
            delete instance.getManagedElements()[block.id];
            block.parentElement.removeChild(block);
            let questions = quest.data.questions;
            questions.splice(questions.indexOf(questions.find(question => question.question_id == block.id)), 1);
        };
        block.append(deleteButton);
    }

    static renderStart(question, instance, sourceEndpoint, position){
        let block = this.renderBlockBase(question, "10rem", "Начало", position);
        instance.manage(block, block.id);
        instance.addEndpoint(block, sourceEndpoint);
        return block;
    }

    static renderFinish(question, instance, targetEndpoint, position){
        let block = this.renderBlockBase(question, "10rem", "Конец", position);
        instance.manage(block, block.id);
        instance.addEndpoint(block, targetEndpoint);
        return block;
    }

    static renderOpenQuestion(quest, question, instance, sourceEndpoint, targetEndpoint, position){
        let block = Render.renderBlockBase(question, "15rem", "Открытый вопрос", position);
        let answerTable = document.createElement("ul");
        answerTable.className = "list-group list-group-flush";
        block.append(answerTable);
        for (let answer of question.answer_options) {
            let tableElement = document.createElement("li");
            tableElement.innerHTML = answer.text;
            tableElement.className = "list-group-item";
            tableElement.id = "answer" + answer.answer_option_id;
            answerTable.append(tableElement);
            instance.addEndpoint(tableElement, {anchor: ["Right", "Left"]}, sourceEndpoint);
        }

        Render.addDeleteButton(quest, block, instance, answerTable.childNodes);

        instance.addEndpoint(block, {anchor: "Top"}, targetEndpoint);

        return block;
    }

    static  renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint, position){
        let block = Render.renderBlockBase(question, "15rem", "Перемещение", position);

        Render.addDeleteButton(quest, block, instance);

        instance.addEndpoint(block, {anchor: "Top"}, targetEndpoint);
        instance.addEndpoint(block, {anchor: "Bottom"}, sourceEndpoint);

        return block;
    }

    static render(quest, instance, sourceEndpoint, targetEndpoint) {
        let position = [0, 0];
        for (let question of quest.data.questions) {
            let block;
            switch (question.type) {
            case "start":
                block = Render.renderStart(question, instance, sourceEndpoint, position);
                break;
            case "end":
                block = Render.renderFinish(question, instance, targetEndpoint, position);
                break;
            case "open":
                block = Render.renderOpenQuestion(quest, question, instance, sourceEndpoint, targetEndpoint, position);
                break;
            case "movement":
                block = Render.renderMovement(quest, question, instance, sourceEndpoint, targetEndpoint, position);
                break;
            case "choice":
                //TODO: change this to function for "choice"
                block = Render.renderOpenQuestion(quest, question, instance, sourceEndpoint, targetEndpoint, position);
                break;
            default:
                break;
            }
        }
        for (let question of quest.data.questions) {
            if (question.type === "start") {
                instance.connect({
                    source: instance.selectEndpoints({element: document.getElementById(question.question_id)}).get(0),
                    target: instance.selectEndpoints({
                        element: document.getElementById(question.answer_options[0].next_question_id)}).get(0)
                });
            }
            else if (question.type === "movement"){
                instance.connect({
                    source: instance.selectEndpoints({element: document.getElementById(question.question_id)}).get(1),
                    target: instance.selectEndpoints({
                        element: document.getElementById(question.movements[0].next_question_id)}).get(0)
                });
            }
            else if (question.type !== "end"){
                for (let answer of question.answer_options) {
                    instance.connect({
                        source: instance.selectEndpoints({
                            element: document.getElementById("answer" + answer.answer_option_id)
                        }).get(0),
                        target: instance.selectEndpoints({
                            element: document.getElementById(answer.next_question_id)
                        }).get(0)
                    });
                }
            }
        }
    }
}
