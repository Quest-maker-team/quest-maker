```json
{
    "quest_id": 0,
    "title": "test1",
    "tags": ["tag1", "tag2"],
    "hidden": false,
    "description": "quest example",
    "password": "",
    "blocks": [
        {
            "block_id": 0,
            "block_text": "start",
            "block_type_name": "start_block",
            "pos_x": 0,
            "pos_y": 0,
            "next_block_id": 1
        },
        {
            "block_id": 1,
            "block_text": "question",
            "block_type_name": "open_question",
            "pos_x": 100,
            "pos_y": 0,
            "media_sources": [
                {
                    "media_id": 0,
                    "media_path": "path",
                    "media_type_name": "image"
                }
            ],
            "next_block_id": null,
            "answers": [
                {
                    "answer_option_id": 0,
                    "text": "answer1",
                    "points": 10,
                    "next_question_id": 2
                }
            ],
            "hints": []
        },
        {
            "block_id": 2,
            "block_text": "question",
            "block_type_name": "choice_question",
            "pos_x": 200,
            "pos_y": 0,
            "media_sources": [
                {
                    "media_id": 1,
                    "media_path": "path",
                    "media_type_name": "audio"
                },
                {
                    "media_id": 2,
                    "media_path": "path",
                    "media_type_name": "audio"
                }
            ],
            "next_block_id": null,
            "answers": [
                {
                    "answer_option_id": 1,
                    "text": "answer1",
                    "points": 10,
                    "next_question_id": 6
                },
                {
                    "answer_option_id": 2,
                    "text": "answer2",
                    "points": 10,
                    "next_question_id": 3
                }
            ],
            "hints": [
                {
                    "hint_id": 0,
                    "hint_text": "hint",
                    "fine": 10,
                    "media_sources": [
                        {
                            "media_id": 3,
                            "media_path": "path",
                            "media_type_name": "image"
                        }
                    ]
                }
            ]
        },
        {
            "block_id": 3,
            "block_text": "movement",
            "block_type_name": "movement",
            "pos_x": 300,
            "pos_y": 100,
            "media_sources": [
                {
                    "media_id": 4,
                    "media_path": "path",
                    "media_type_name": "image"
                }
            ],
            "next_block_id": 4,
            "hints": [],
            "place": {
                "place_id": 0,
                "latitude": 100,
                "longitude": 200,
                "radius": 10,
                "time_open": "", 
                "time_close": ""
            }
        },
        {
            "block_id": 4,
            "block_text": "movement",
            "block_type_name": "movement",
            "pos_x": 400,
            "pos_y": 100,
            "media_sources": [
                {
                    "media_id": 5,
                    "media_path": "path",
                    "media_type_name": "audio"
                }
            ],
            "next_block_id": 5
        },
        {
            "block_id": 5,
            "block_text": "end",
            "block_type_name": "end_block",
            "pos_x": 600,
            "pos_y": 0,
            "next_block_id": null
        }
    ]
}
```