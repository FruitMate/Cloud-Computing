# Cloud Computing - FruitMate

## API Description
RESTful APIs deployed on Google Cloud Platform using the services of App Engine, Google Cloud Storage, Firebase Authentication, and Firestore in Firebase. This API functions to take requests and then process data on the server side and return responses back to the user.

## Stacks
- Python
- Flask Framework
- App Engine (Google Cloud Platform)
- Google Cloud Storage (Google Cloud Platform)
- Firebase Authentication (Google Cloud Platform)
- Firebase Firestore (Google Cloud Platform)
- Postman

## Team Member
The following are the team members involved in the development of this project:

| Name | Student-ID | Learning Path | Role | Contacts |
| :-------- | :------- | :-------------------------------- | :-------- | :-------- |
| Riesco Alief Frendnanda Editya | M207DSX2302 | Machine Learning | Project Manager & Machine Learning Engineer | LinkedIn & Github |
| Noraini Latifah | M207DSY3260 | Machine Learning | Machine Learning Engineer | LinkedIn & Github |
| I Wayan Guna Permana | C368DSX2417 | Cloud Computing | DevOps Engineer | LinkedIn & Github |
| Anak Agung Made Semara Putra | C368DSX2788 | Cloud Engineer | DevOps Engineer | LinkedIn & Github |
| I Gusti Agung Ngurah Fajar Dharmawangsa | A013DSX1415 | Mobile Development | Android Developer | LinkedIn & Github |
| Muhammad Rafif Baihaqi | A013DSX1421 | Mobile Development | Android Developer | LinkedIn & Github |


## API Endpoints

### URL: 

### 1. Endpoint: `/`
#### Running Test
- *Method*: GET
- *Header*: -
- *Request Body*: -
- *Response*:
  ```json
  {
    "message": "Application running!"
  }
  ```
  
### 2. Endpoint: `/api/scan-apple`
#### Endpoint to receive requests and provide responses to fruit classification
- *Method*: POST
- *Header*: 
  - **`Content-Type: multipart/form-data`**
- *Request Body*:
  - **`-`**
- *Response*:
  ```json
  {
    "code": 200,
    "message": "Classification Success!",
    "prediction": "overripe"
  }
  ```
  
### 3. Endpoint: `/api/history/[param]`
#### Endpoint to receive requests and provide responses to fruit classification
- *Method*: GET
- *Header*: 
  - **`-`**
- *Request Body*:
  - **`-`**
- *Request Params*:
  | Parameter | Type    | Description               |
  | :-------- | :------ | :------------------------ |
  | Email     | String  | Authenticated user email  |

- *Response*:
  ```json
  {
    "code": 200,
    "data": [
        {
            "uid": "iYqXpePAHAd97Rwum1lNMPpTk234",
            "classification_result": "overripe",
            "timestamp": "2023-06-07 15:43:59",
            "image_url": "https://storage.googleapis.com/img-history-storage-bucket/20230607154356_iYqXpePAHAd97Rwum1lNMPpTk2N2_0TjqBkd6WD.jpg"
        },
        {
            "uid": "iYqXpePAHAd97Rwum1lNMPpTk234",
            "classification_result": "unripe",
            "timestamp": "2023-06-07 15:56:07",
            "image_url": "https://storage.googleapis.com/img-history-storage-bucket/20230607155606_iYqXpePAHAd97Rwum1lNMPpTk2N2_yqVBs0lM1V.jpg"
        },
        {
            "uid": "iYqXpePAHAd97Rwum1lNMPpTk234",
            "classification_result": "ripe",
            "timestamp": "2023-06-07 15:22:19",
            "image_url": "https://storage.googleapis.com/img-history-storage-bucket/20230607152212_iYqXpePAHAd97Rwum1lNMPpTk2N2_XCaFE0odhY.jpg"
        },
        {
            "uid": "iYqXpePAHAd97Rwum1lNMPpTk234",
            "classification_result": "ripe",
            "timestamp": "2023-06-07 15:40:43",
            "image_url": "https://storage.googleapis.com/img-history-storage-bucket/20230607154040_iYqXpePAHAd97Rwum1lNMPpTk2N2_qezPXcnajK.jpg"
        }
    ]
  }
  ```
