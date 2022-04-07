export function RenderBlock(id, width, cardBody){
    let block = document.createElement("div");
    block.id = id;
    block.className = "position-absolute border-2 card";

    let blockBody = document.createElement("div");
    blockBody.className = "card-body";
    blockBody.innerHTML = cardBody;
    block.style.width = width;
    block.append(blockBody);

    document.getElementById("container").append(block);
    return block;
}

export function AddDeleteButton(block, answerElements, instance){
    let deleteButton = document.createElement("button");
    deleteButton.id = "btn" + block.id;
    deleteButton.className = "btn-close";
    deleteButton.onclick = function (){
        console.log("delete");
        for (let answerElement of answerElements) {
            instance.deleteConnectionsForElement(answerElement);
            instance.selectEndpoints({element: answerElement}).deleteAll();
        }
        instance.deleteConnectionsForElement(block);
        instance.selectEndpoints({element: block}).deleteAll();
        block.parentElement.removeChild(block);
    }
    block.append(deleteButton);
}

export function RenderStart(question, instance, sourceEndpoint){
    let content = "<h5 class=\"card-title text-center\">Start</h5>" +
                    "<hr>" +
                    "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
    let block = RenderBlock(question.question_id, "10rem", content);
    instance.manage(block, block.id);
    instance.addEndpoint(block, sourceEndpoint);
}

export function RenderFinish(question, instance, targetEndpoint){
    let content = "<h5 class=\"card-title text-center\">Finish</h5>" +
                    "<hr>" +
                    "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
    let block = RenderBlock(question.question_id, "10rem", content);
    instance.manage(block, block.id);
    instance.addEndpoint(block, targetEndpoint);
}

export function RenderOpenQuestion(question, instance, sourceEndpoint, targetEndpoint){
    let content = "<h5 class=\"card-title text-center\">Open</h5>" +
                    "<hr>" +
                    "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
    console.log(question.answer_options);
    let block = RenderBlock(question.question_id, "15rem", content);

    let answerTable = document.createElement("ul");
    answerTable.className = "list-group list-group-flush";
    for (let answer of question.answer_options) {
        let tableElement = document.createElement("li");
        tableElement.innerHTML = answer.text;
        tableElement.className = "list-group-item";
        answerTable.append(tableElement);
        instance.addEndpoint(tableElement, {anchor: ["Right", "Left"]}, sourceEndpoint);
    }
    block.append(answerTable);

    AddDeleteButton(block, answerTable.childNodes, instance);

    instance.manage(block, block.id);
    instance.addEndpoint(block, targetEndpoint);

}

export function Render(quest, instance, sourceEndpoint, targetEndpoint) {
    RenderStart(quest.questions.find(question => question.type === "start"), instance, sourceEndpoint);
    RenderFinish(quest.questions.find(question => question.type === "end"), instance, targetEndpoint);
    //console.log(quest.questions.find(question => question.type === "open"));
    RenderOpenQuestion(quest.questions.find(question => question.type === "open"), instance, sourceEndpoint, targetEndpoint);
}