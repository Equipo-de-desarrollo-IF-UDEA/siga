import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EditRoutingModule } from './edit-routing.module';
import { EditComponent } from './edit.component';
import { CommissionComponent } from './components/commission/commission.component';
import { PermissionComponent } from './components/permission/permission.component';
import { SharedModule } from '@shared/shared.module';


@NgModule({
  declarations: [
    EditComponent,
    CommissionComponent,
    PermissionComponent
  ],
  imports: [
    CommonModule,
    EditRoutingModule,
    SharedModule
  ]
})
export class EditModule { }
