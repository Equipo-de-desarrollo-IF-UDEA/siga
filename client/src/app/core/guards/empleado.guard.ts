//angular
import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  CanActivate,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';

//rxjs
import { Observable } from 'rxjs';

//services
import { AuthService } from '@services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class EmpleadoGuard implements CanActivate {
  constructor(private authSvc: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ):
    | Observable<boolean | UrlTree>
    | Promise<boolean | UrlTree>
    | boolean
    | UrlTree {
    if (!this.authSvc.isLoggedIn()) {
      console.log('esta en guard')
      this.router.navigate(['auth/login']);
    }
    return this.authSvc.isLoggedIn();
  }
}
