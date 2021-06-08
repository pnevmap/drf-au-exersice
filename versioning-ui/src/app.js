import { PLATFORM } from "aurelia-framework";
import { UserSession } from './user-session';
import { inject } from 'aurelia-framework';
import { Redirect } from 'aurelia-router';


@inject(UserSession)
export class App {
  constructor(userSession) {
    this.userSession = userSession;
  }

  configureRouter(config, router) {
    config.title = 'Aurelia';
    config.addAuthorizeStep(AuthorizeStep);
    config.map([
      { route: ['', 'home'], name: 'home', moduleId: PLATFORM.moduleName('home'), title: 'home', nav: true, settings: { auth: true } },
      { route: 'revisions', name: 'revisions', moduleId: PLATFORM.moduleName('revisions'), title: 'revisions', nav: true, settings: { auth: true } },

    ]);

  }


  logoutAction() {
    this.userSession.currentUser = undefined;
    window.sessionStorage.removeItem('versioning-ui-user');
    window.location.href = '/api-auth/login/';
  }


}
@inject(UserSession)
class AuthorizeStep {
  constructor(userSession) {
    this.userSession = userSession;
  }
  run(navigationInstruction, next) {
    if (navigationInstruction.getAllInstructions().some(i => i.config.settings.auth)) {
      var isAuthenticated = this.userSession.isLoggedIn();
      if (!isAuthenticated) {
        //alert('going back');
        window.location.href = '/api-auth/login/';
        return next.cancel(new Redirect('login'));
      }
    }

    return next();
  }
}



