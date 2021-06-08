import { UserSession } from './user-session';
import { inject } from 'aurelia-framework';
import { HttpClient } from 'aurelia-http-client';

@inject(UserSession)
export class Home {
  constructor(userSession) {
    this.documents = [];
    this.toUpload = { "url": "", "file": "" };
    this.userSession = userSession;
  }

  created() {
    this.loadRevisions();
  }

  loadRevisions() {
    //TODO consider abstracting these http calls to avoid code duplication
    let httpClient = new HttpClient();
    httpClient.createRequest('/documents/')
      .asGet()
      .withCredentials(true)
      .withHeader('X-CSRFToken', this.userSession.getCookie('csrftoken'))
      .send()
      .then(data => {
        console.log(data);
        this.documents = data.content;
      }).catch(err => {
        console.log(err);
        window.location.href = '/api-auth/login/';
      });
  }

  uploadAction(toUpload) {
    //TODO consider abstracting these http calls to avoid code duplication
    let httpClient = new HttpClient();
    var form = new FormData();
    form.append('url', toUpload.url);
    form.append('file', toUpload.file[0]);
    httpClient.createRequest('/documents/')
      .asPost()
      .withCredentials(true)
      .withHeader('X-CSRFToken', this.userSession.getCookie('csrftoken'))
      .withContent(form)
      .send()
      .then(response => {
        console.log(response.response);
        this.loadRevisions();
      })
      .catch(err => {
        console.log(err);
      });
  }

  uploadRevisionAction(toUploadRevision) {
    //TODO consider abstracting these http calls to avoid code duplication
    let httpClient = new HttpClient();
    var form = new FormData();
    form.append('url', toUploadRevision.url);
    form.append('file', toUploadRevision.file[0]);
    httpClient.createRequest('/documents/')
      .asPut()
      .withCredentials(true)
      .withContent(form)
      .withHeader('X-CSRFToken', this.userSession.getCookie('csrftoken'))
      .send()
      .then(response => {
        console.log(response.response);
        this.loadRevisions();
      })
      .catch(err => {
        console.log(err);
      });
  }
}
