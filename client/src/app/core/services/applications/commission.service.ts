import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@environments/environment';
import { CommissionCreate, CommissionResponse, ComplimentCreate } from '@interfaces/applications/commission';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommissionService {

  private urlEndPoint: string = environment.route + 'commission/'

  constructor(
    private http: HttpClient
  ) { }

  getCommission(id: number): Observable<CommissionResponse> {
    return this.http.get<CommissionResponse>(this.urlEndPoint + id)
  }

  postCommission(body: CommissionCreate): Observable<CommissionResponse> {
    return this.http.post<CommissionResponse>(this.urlEndPoint, body)
  }

  putCommission(body: CommissionCreate, id: number) {
    return this.http.put(this.urlEndPoint + id, body)
  }

  deleteCommission(id: number){
    return this.http.delete(this.urlEndPoint + id)
  }

  putCompliment(body: ComplimentCreate, id: number) {
    return this.http.put(this.urlEndPoint + 'compliment/' + id, body)
  }

}
