function makeRequest(method, url, data) {
    return new Promise(function(resolve, reject) {
        const xmlhttp = new XMLHttpRequest();
        xmlhttp.open(method, url);
        xmlhttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

        xmlhttp.onreadystatechange = () => {
            if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                if (xmlhttp.status === 200) {
                    resolve(xmlhttp.response);
                } else {
                    // console.log(xmlhttp.responseText);
                    reject(xmlhttp.status);
                }
            }
        };

        if (data !== undefined) {
            xmlhttp.send(data);
        } else {
            xmlhttp.send();
           }
    });
}

function load(offset, limit) {
    //console.log(offset, limit);
    return makeRequest('GET', 'api/catalog/quests' +
                                        '?offset=' + offset.toString() +
                                        '&limit=' + limit.toString()).then((result) => {
        return JSON.parse(result);
    });
}

function addPagination(limit, offset) {
        const pagination = document.getElementById('pagination');
        pagination.insertAdjacentHTML('beforeend',
        '<li class="page-item ' + ((offset - limit < 0)?'disabled':'') + '">' +
                '<a class="page-link" ' +
                    'href="/catalog.html?offset=' + (offset - limit).toString() + '&limit=' + limit.toString() + '"' +
                    ' aria-label="Предыдущая">' +
                    '<span aria-hidden="true">&laquo;</span>' +
                '</a>' +
            '</li>');
            if (offset > limit * 2) {
                pagination.insertAdjacentHTML('beforeend',
                    '<li class="page-item disabled"><a class="page-link">...</a></li>');
            }
            if (offset > limit) {
                pagination.insertAdjacentHTML('beforeend',
                '<li class="page-item">' +
                    '<a class="page-link" ' +
                        'href="/catalog.html?offset=' + (offset - limit * 2).toString() + '&limit=' + limit.toString() + '">' +
                        (offset / limit - 1) + '</a>' +
                '</li>');
            }
            if (offset >= limit) {
                pagination.insertAdjacentHTML('beforeend',
                '<li class="page-item">' +
                    '<a class="page-link" ' +
                        'href="/catalog.html?offset=' + (offset - limit).toString() + '&limit=' + limit.toString() + '">' +
                        (offset)/limit + '</a>' +
                '</li>');
            }
            pagination.insertAdjacentHTML('beforeend',
            '<li class="page-item active">' +
                '<a class="page-link" href="/catalog.html?offset=' + offset + '&limit=' + limit.toString() + '">' +
                (offset / limit + 1) + '</a>' +
            '</li>' +

            '<li class="page-item">' +
                '<a class="page-link" ' +
                    'href="/catalog.html?offset=' + (offset + limit).toString() + '&limit=' + limit.toString() + '">' +
                    (offset / limit + 2) + '</a>' +
            '</li>' +

            '<li class="page-item disabled"><a class="page-link">...</a></li>' +

            '<li class="page-item">' +
                '<a class="page-link"' +
                    'href="/catalog.html?offset=' + (offset + limit).toString() + '&limit=' + limit.toString() + '"' +
                    ' aria-label="Следующая">' +
                    '<span aria-hidden="true">&raquo;</span>' +
                '</a>' +
            '</li>');
}

function addTags() {
    const filters = document.getElementById('filters');
    makeRequest('GET', 'api/catalog/tags').then((result) => {
        tags = JSON.parse(result).tags;
        console.log(tags);
        for (const tagInd in tags){
            filters.insertAdjacentHTML('beforeend',
                '<div class="form-check">' +
                    '<input class="form-check-input" type="checkbox" value="" id=' + tagInd + '>' +
                    '<label class="form-check-label" for=' + tagInd + '>' + tags[tagInd] + '</label>' +
                '</div>');
        }
    });
}

window.onload = () => {
    const query = window.location.href.split('?')[1];
    const queryParams = query.split('&');
    const offset = parseInt(queryParams[0].split('=')[1]);
    const limit = parseInt(queryParams[1].split('=')[1]);
    load(offset, limit).then((result) => {
        console.log(result);
        const container = document.getElementById('container');
        for (const quest of result.quests) {
            container.insertAdjacentHTML('beforeend',
                '<div class="card">' +
                    '<div class="card-body">' +
                        '<h5 class="card-title">' + quest.title + '</h5>' +
                        '<h6 class="card-subtitle mb-2 text-muted">Автор: ' + quest.author + '</h6>' +
                        '<p class="card-text" style="overflow: hidden;' +
                                                    'display: -webkit-box;' +
                                                    '-webkit-line-clamp: 5;\n' +
                                                    '-webkit-box-orient: vertical;\n' +
                                                    'line-height: 1.3em;\n' +
                                                    'height: 6.6em;">' +
                            quest.description +
                        '</p>' +
                        '<p class="card-text"> ID: ' +
                        quest.keyword +
                        '</p>' +
                        '<a href="#" class="btn btn-primary">Подробнее</a>' +
                    '</div>\n' +
                '</div>');
        }
        addPagination(limit, offset);
        addTags();
    });
};