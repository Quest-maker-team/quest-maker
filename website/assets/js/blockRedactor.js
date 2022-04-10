export function init () {
    console.log("In init map");
    
    myMap = new ymaps.Map("map", {
        center: [57.5262, 38.3061], // Углич
        zoom: 11
    }, {
        balloonMaxWidth: 200,
        searchControlProvider: 'yandex#search'
    });
    console.log(myMap);
    // Обработка события, возникающего при щелчке
    // левой кнопкой мыши в любой точке карты.
    // При возникновении такого события откроем балун.
    myMap.events.add('click', function (e) {
        if (!myMap.balloon.isOpen()) {
            let coords = e.get('coords');
            myMap.balloon.open(coords, {
                contentHeader:'Событие!',
                contentBody:'<p>Кто-то щелкнул по карте.</p>' +
                    '<p>Координаты щелчка: ' + [
                    coords[0].toPrecision(6),
                    coords[1].toPrecision(6)
                    ].join(', ') + '</p>',
                contentFooter:'<sup>Щелкните еще раз</sup>'
            });
        }
        else {
            myMap.balloon.close();
        }
    });

    // Обработка события, возникающего при щелчке
    // правой кнопки мыши в любой точке карты.
    // При возникновении такого события покажем всплывающую подсказку
    // в точке щелчка.
    myMap.events.add('contextmenu', function (e) {
        myMap.hint.open(e.get('coords'), 'Кто-то щелкнул правой кнопкой');
    });
    
    // Скрываем хинт при открытии балуна.
    myMap.events.add('balloonopen', function (e) {
        myMap.hint.close();
    });
}
export class BlockRedactor {
    static addTextRedactor(form, label, text){
        form.innerHTML +=
            "<label for=\"formControlTextarea\" class=\"form-label\">" + label + "</label>" +
            "<textarea class=\"form-control\" id=\"formControlTextarea\" rows=\"3\"> " +
            text +
            "</textarea>";
    }

    static addAnswerForOpenQuestion(form, answer){
        form.innerHTML +=
            "<div class='col-8'>"+
                "<input type=\"text\" class=\"form-control\" value=" + answer.text + ">" +
            "</div>" +
            "<div class=\"col-3\">" +
                "<div class='input-group'>" +
                    "<span class=\"input-group-text\"> Очки </span>" +
                    "<input type=\"text\" class=\"form-control\" value=" + answer.points + ">" +
                "</div>" +
            "</div>" +
            "<div class='col-1'>" +
                "<button class=\"btn btn-danger\">-</button>" +
            "</div>"
    }
    static addMovementForMovementBlock(form, question){
        form.innerHTML +=
            "<div class='col-8'>"+
                "<div class='input-group'>" +
                    "<span class=\"input-group-text\"> Координаты </span>" +
                    "<input type=\"text\" class=\"form-control\" id=\"moveCoords\" value=" + question.movements[0].place.coords + ">" +
                "</div>"+
                "<div class='input-group'>" +
                    "<span class=\"input-group-text\"> Радиус(м) </span>" +
                    "<input type=\"text\" class=\"form-control\" id=\"moveRadius\"  value=" +question.movements[0].place.radius + ">" +
            "<div class=\"col-3\">" +
                "<div class='input-group'>" +
                    "<span class=\"input-group-text\"> Очки </span>" +
                    "<input type=\"text\" class=\"form-control\" id=\"movePoints\"  value=" + question.answer_options[0].points + ">" +
                "</div>" +
            "</div>";
    }
    static createStartRedactor(form, question){
        this.addTextRedactor(form, "Приветственное сообщение:", question.text);
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createFinishRedactor(form, question){
        this.addTextRedactor(form, "Прощальное сообщение:", question.text);
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createOpenQuestionRedactor(form, question){
        this.addTextRedactor(form, "Вопрос", question.text);
        form.innerHTML += "<hr><label for=\"formControlTextarea\" class=\"form-label\">Ответы:</label>";
        for (let answer of question.answer_options) {
            this.addAnswerForOpenQuestion(form, answer);
        }
        form.innerHTML += "<div class='col-auto'><button type='button' class='btn btn-primary'>Добавить ответ</button></div>";
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createMovementRedactor(form, question){

        this.addTextRedactor(form, "Перемещение", question.text);
        form.innerHTML+='<style>'+
        'html, body, #map {'+
        '    width: 100%; height:466px; padding: 0; margin: 0;'+
        '}'+
        '</style>'+
        '<div id="map"></div>';
        let myMap;
        let mapId = document.getElementById("map");
        console.log(mapId);
        ymaps.ready (function () {
            myMap   = new ymaps.Map("map", {
                center: [57.5262, 38.3061], 
                zoom: 11
            }, {
                balloonMaxWidth: 200,
                searchControlProvider: 'yandex#search'
            });
            console.log(myMap);
            myMap.events.add('click', function (e) {
                if (!myMap.balloon.isOpen()) {
                    let coords = e.get('coords');
                    myMap.balloon.open(coords, {
                        contentHeader:'Новое место квеста',
                        contentBody:'<p></p>' +
                            '<p>Координаты точки: ' + [
                            coords[0].toPrecision(6),
                            coords[1].toPrecision(6)
                            ].join(', ') + '</p>',
                        contentFooter:'<sup>Вы можете выбрать новую точку</sup>'
                    });
                    //console.log(coords[0]);
                    question.movements[0].place.coords ="("+coords[0].toString()+","+coords[1].toString()+")";
                    console.log( question.movements[0].place.coords);
                    document.getElementById("moveCoords").value = question.movements[0].place.coords;
                }
                else {
                    myMap.balloon.close();
                }
            });
            
            myMap.events.add('balloonopen', function (e) {
                myMap.hint.close();
            });;
        });
        console.log(myMap);
        BlockRedactor.addMovementForMovementBlock(form, question);
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
            question.movements[0].place.coords = document.getElementById("moveCoords").value;
            question.movements[0].place.radius = document.getElementById("moveRadius").value;
            question.answer_options[0].points = document.getElementById("movePoints").value;
        };
    }

    static showRedactor(question){
        let modal = new bootstrap.Modal(document.getElementById("redactor"));
        let form = document.getElementById("redactorForm");
        form.innerHTML = "";
        switch (question.type) {
            case "start":
                this.createStartRedactor(form, question);
                break;
            case "end":
                this.createFinishRedactor(form, question);
                break;
            case "open":
                this.createOpenQuestionRedactor(form, question);
                break;
            case "movement":
                this.createMovementRedactor(form, question);
                break;
            default:
                break;
        }
        modal.show();
    }
}
