import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


interface LoginResponse {
  access_token: string;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';

  constructor(private http: HttpClient, private router: Router) { }

  onSubmit() {
    const url = 'http://127.0.0.1:8081/user/login';
    const body = { email: this.email, password: this.password };

    this.http.post<LoginResponse>(url, body).subscribe(response => {
      localStorage.setItem('token', response.access_token);
      this.router.navigateByUrl('/chat',);
    },error => {
      // Handle login error (e.g., display error message)
      alert(`Login failed: ${error}`);
    });
  }
}