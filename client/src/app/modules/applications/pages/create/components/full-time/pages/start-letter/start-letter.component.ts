import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-start-letter',
  templateUrl: './start-letter.component.html',
  styleUrls: ['./start-letter.component.scss']
})
export class StartLetterComponent implements OnInit {

  @Input() idDedication: number | string = 0;
  @Input() editable: any;

  cartaInicio: any;

  fecha = new Date();

  usuario:any;
  

  constructor() { }

  ngOnInit(): void {
  }

}
