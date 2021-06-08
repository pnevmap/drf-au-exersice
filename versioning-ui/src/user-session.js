import { HttpClient } from 'aurelia-http-client';

export class UserSession {

  isLoggedIn() {
    //    this.currentUser = 'admin';
    //    return true;
    if (!Object.is(this.currentUser, undefined)) {
      return true;
    }

    let sessionUser = window.sessionStorage.getItem('versioning-ui-user');
    if (sessionUser != null) {
      this.currentUser = sessionUser;
      return true;
    } else {
      this.whoami();
      return true;//once i m here, i m authenticated!
    }
  }

  whoami() {
    let httpClient = new HttpClient();
    httpClient.createRequest('/whoami/')
      .asGet()
      .withCredentials()
      .send()
      .then(response => {
        this.currentUser = response.content.username;
        window.sessionStorage.setItem('versioning-ui-user', this.currentUser);
      })
      .catch(err => {
        console.log(err);
      });
  }

  getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
}
