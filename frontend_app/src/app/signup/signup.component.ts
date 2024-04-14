import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

interface SignUpResponse {
  access_token: string;
}

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  fullname = '';
  email = '';
  password = '';

  constructor(private http: HttpClient) { }
  signUp() {
    const url = 'http://127.0.0.1:8081/user/signup';
    const body = {fullname:this.fullname, email: this.email, password: this.password };

    this.http.post<SignUpResponse>(url, body).subscribe(response => {
      localStorage.setItem('token', response.access_token);
    });
  }
}