import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@environments/environment';
import { CommissionResponse } from '@interfaces/applications/commission';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommissionService {

  private urlEndPoint: string = environment.rute + 'commission/'

  constructor(
    private http: HttpClient
  ) { }

  getCommission(id: number): Observable<CommissionResponse> {
    return this.http.get<CommissionResponse>(this.urlEndPoint+id)
  }

}
