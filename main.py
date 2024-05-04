from flask import Blueprint

main= Blueprint(__name__, "main")

@main.route("/")
def home():
    return "Welcome to RailwayGo "
