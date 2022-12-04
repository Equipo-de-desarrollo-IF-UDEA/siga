//angular
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

//component
import { HomeComponent } from './pages/home/home.component';
import { CreateApplicationComponent } from './pages/create-application/create-application.component';
import { NotFoundComponent } from '@shared/components/not-found/not-found.component';
import { EmpleadoGuard } from 'src/app/core/guards/empleado.guard';

const routes: Routes = [
  { path: '', component: HomeComponent },
  {
    path: 'create-application',
    canActivate: [EmpleadoGuard],
    component: CreateApplicationComponent,
  },
  { path: 'not-found', component: NotFoundComponent },
  { path: '**', redirectTo: '/home'},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class HomeRoutingModule {}
