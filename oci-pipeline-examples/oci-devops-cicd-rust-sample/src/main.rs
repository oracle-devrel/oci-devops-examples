#![feature(decl_macro)]

#[macro_use] extern crate rocket;

use rocket::Request;
use rocket::response::content::Json;


#[get("/hello")]
fn hello() -> Json<&'static str> {
  Json("{
    'status': 'In',
    'message': 'Hello World with RUST & Rocket!'
  }")
}

#[catch(404)]
fn not_found(req: &Request) -> String {
    print!("{}", req);
    format!("Sorry path not available '{}'", req.uri())
}


fn main() {
  rocket::ignite()
    .register(catchers![not_found])
    .mount("/v0", routes![hello])
    .launch();
}