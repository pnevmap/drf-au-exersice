import { UserSession } from './user-session';
import { inject } from 'aurelia-framework';
import { HttpClient } from 'aurelia-http-client';

@inject(UserSession)
export class Revisions {
  constructor(userSession) {
    this.userSession = userSession;
  }

  created() {
    this.loadRevisions();
  }
  activate(params) {
    console.log(params.url);
    this.url = params.url;
  }
  loadRevisions() {
    let httpClient = new HttpClient();

    httpClient.createRequest('/documents/' + this.url + '/revisions/')
      .asGet()
      //.withHeader('Authorization', 'Token ' + this.userSession.authToken)
      .withCredentials(true)
      .send()
      .then(data => {
        console.log(data);
        this.revisions = data.content[0];
      }).catch(err => {
        console.log(err);
      });
  }
}
