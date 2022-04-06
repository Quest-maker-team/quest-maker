export function RenderBlock(id, content){
    let block = document.createElement("div");
    block.id = id;
    block.className = "position-absolute border-2 card";

    let blockBody = document.createElement("div");
    blockBody.className = "card-body";
    blockBody.innerHTML = content;

    block.append(blockBody);

    document.getElementById("container").append(block);
    return block;
}

export function RenderStart(question, instance){
    let content = "<h5 class=\"card-title text-center\" style=\"width: 10rem\">Start</h5>" +
                    "<hr>" +
                    "<p class=\"card-text text-center\">"+ question.text +"</p>";
    let block = RenderBlock(question.question_id, content);
    instance.manage(block, block.id);
}

export function Render(quest, instance){
    //let welcomeMessage = quest.questions.find(question => question.type === "start").text;
    RenderStart(quest.questions.find(question => question.type === "start"), instance);
    //console.log(welcomeMessage);
}