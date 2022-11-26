import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import Swal from 'sweetalert2';
import { AuthService } from '@services/auth.service';
import { Msg } from '@interfaces/msg';

@Injectable()
export class ErrorsInterceptor implements HttpInterceptor {

  constructor(
    private authService: AuthService
  ) { }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError(
        (_error: HttpErrorResponse) => {
          let errMsg = '';
          if (_error.status == 500) {
            Swal.fire({
              title: 'Error del servidor',
              text: _error.error.detail,
              confirmButtonText: 'Aceptar',
              icon: 'error'
            })
          } else {
            if (_error.status == 422) {
              console.log(_error)
              Swal.fire({
                title: 'Error',
                text: _error.error.detail[0].msg,
                confirmButtonText: 'Aceptar',
                icon: 'error'
              })
            } else {
              Swal.fire({
                title: 'Error',
                text: _error.error.detail,
                confirmButtonText: 'Aceptar',
                icon: 'error'
              }).then(
                result => {
                  if (result.isConfirmed){
                    if (_error.error.detail == "Tu cuenta no se encuentra activa, recuerda revisar tu correo para activarla o pide correo de activación nuevamente") {
                      Swal.fire({
                        title: 'Enviar correo de activación',
                        text: 'Correo o cédula:',
                        input: 'text',
                        inputAttributes: {
                          autocapitalize: 'off'
                        },
                        showCancelButton: true,
                        confirmButtonText: 'Enviar',
                        showLoaderOnConfirm: true,
                        preConfirm: (email) => {
                          return this.authService.sendActivateEmail(email).subscribe(
                            (res: Msg) => {
                              Swal.fire({
                                title: "Correo de activación",
                                text: res.msg,
                                icon: 'success'
                              })
                            }
                          )
                        },
                        allowOutsideClick: () => !Swal.isLoading()
                      })
                    }
                  }
                }
              )
            }

          }
          return throwError(_error.error.message);
        }
      )
    );
  }
}
