import _ from 'underscore';

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

function load(offset, limit, tags, title) {
    let url = 'api/catalog/quests' +
              '?offset=' + offset.toString() +
              '&limit=' + limit.toString();
    if (title !== null)
        url += '&title=' + title;
    for (const tag of tags) {
        url += '&tags=' + tag;
    }
    return makeRequest('GET', url).then((result) => {
        return JSON.parse(result);
    });
}

function addPagination(limit, offset, total, tags) {
        const pagination = document.getElementById('pagination');
        let tagsParams = '';
        for (const tag of tags){
            tagsParams += '&tags=' + tag;
        }
        pagination.insertAdjacentHTML('beforeend',
        '<li class="page-item ' + ((offset - limit < 0)?'disabled"':'"') + '>' +
                '<a class="page-link" ' +
                    'href="/catalog.html?offset=' + (offset - limit).toString() + '&limit=' + limit.toString() + tagsParams + '"' +
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
                        'href="/catalog.html?offset=' + (offset - limit * 2).toString() + '&limit=' + limit.toString() + tagsParams + '">' +
                        (offset / limit - 1) + '</a>' +
                '</li>');
        }
        if (offset >= limit) {
            pagination.insertAdjacentHTML('beforeend',
                '<li class="page-item">' +
                    '<a class="page-link" ' +
                        'href="/catalog.html?offset=' + (offset - limit).toString() + '&limit=' + limit.toString() + tagsParams + '">' +
                        (offset)/limit + '</a>' +
                '</li>');
        }

        pagination.insertAdjacentHTML('beforeend',
            '<li class="page-item active">' +
                '<a class="page-link" href="/catalog.html?offset=' + offset + '&limit=' + limit.toString() + tagsParams + '">' +
                (offset / limit + 1) + '</a>' +
            '</li>');

        if (offset + limit < total) {
            pagination.insertAdjacentHTML('beforeend',
                '<li class="page-item">' +
                    '<a class="page-link" ' +
                        'href="/catalog.html?offset=' + (offset + limit).toString() + '&limit=' + limit.toString() + tagsParams + '">' +
                        (offset / limit + 2) + '</a>' +
                '</li>');
        }
        if (offset + limit * 2 < total) {
            pagination.insertAdjacentHTML('beforeend',
                '<li class="page-item disabled"><a class="page-link">...</a></li>');
        }

        pagination.insertAdjacentHTML('beforeend',
            '<li class="page-item ' + ((offset + limit > total)?'disabled"':'"') + '>' +
                '<a class="page-link"' +
                    'href="/catalog.html?offset=' + (offset + limit).toString() + '&limit=' + limit.toString() + tagsParams + '"' +
                    ' aria-label="Следующая">' +
                    '<span aria-hidden="true">&raquo;</span>' +
                '</a>' +
            '</li>');
}

function addTags(offset, limit, chekedTag) {
    const filters = document.getElementById('filters');
    const usedFilters = document.getElementById("usedFilters");
    return makeRequest('GET', 'api/catalog/tags').then((result) => {
        let tags = JSON.parse(result).tags;
        console.log(tags);
        for (const tagInd in tags){
            filters.insertAdjacentHTML('beforeend',
                '<div class="form-check">' +
                    '<input class="form-check-input" type="checkbox" value="" id=tag' + tagInd + '>' +
                    '<label class="form-check-label" for=tag' + tagInd + '>' + tags[tagInd] + '</label>' +
                '</div>');
        }
        for (const tag of chekedTag){
            document.getElementById('tag' + tags.findIndex((find) => find === tag)).checked = true;

            usedFilters.insertAdjacentHTML('beforeend', '<div class="mx-1"><span class="badge bg-primary">' + tag + '</span></div>');
        }
        document.getElementById('reset').onclick = () => {
            for (const tagInd in tags) {
                document.getElementById('tag' + tagInd).checked = false;
            }
        };
        document.getElementById('apply').onclick = () => {
            let url = '/catalog.html' +
                    '?offset=' + offset.toString() +
                    '&limit=' + limit.toString();
            for (const tagInd in tags) {
                if (document.getElementById('tag' + tagInd).checked)
                    url += '&tags=' + tags[tagInd];
            }
            document.location = url;
        }
    });
}

window.onload = () => {
    const query = window.location.href.split('?')[1];
    const queryParams = query.split('&');
    const offset = parseInt(queryParams[0].split('=')[1]);
    const limit = parseInt(queryParams[1].split('=')[1]);
    let title = null;
    const tags = [];

    for (const param of queryParams){
        if (param.split('=')[0] === 'tags')
            tags.push(param.split('=')[1]);
        else if (param.split('=')[0] === 'title')
            title = param.split('=')[1];
    }
    load(offset, limit, tags, title).then((result) => {
        console.log(result);
        const container = document.getElementById('container');
        for (const quest of result.quests) {
            container.insertAdjacentHTML('beforeend',
                '<div class="col">' +
                '<div class="card h-100">' +
                    '<div class="card-body">' +
                        '<h5 class="card-title">' + quest.title + '</h5>' +
                        '<h6 class="card-subtitle mb-2 text-muted">Автор: ' + quest.author + '</h6>' +
                        '<div class="card-text" style="white-space: pre-wrap;' +
                                                'overflow: hidden;' +
                                                'display: -webkit-box;' +
                                                '-webkit-line-clamp: 5;\n' +
                                                '-webkit-box-orient: vertical;\n' +
                                                'line-height: 1.3em;\n' +
                                                'height: 6.6em;">' +
                            quest.description +
                        '</div>' +
                        '<p class="card-text"> ID: ' +
                            quest.keyword +
                        '</p>' +
                        '<!--<a href="#" class="btn btn-primary">Подробнее</a>-->' +
                    '</div>' +
                '</div>' +
            '</div>');
            }
        addPagination(limit, offset, result.total, tags);
        addTags(offset, limit, tags);

        document.getElementById('searchButton').onclick = () => {
            document.location = '/catalog.html' +
                    '?offset=' + offset.toString() +
                    '&limit=' + limit.toString() +
                    '&title=' + _.escape(document.getElementById('search').value);
        }
    });
};