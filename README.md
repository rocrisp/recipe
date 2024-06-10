clone the repository

#change to recipe-app dir
$ cd recipe-app

# Build the container image
$ podman build --platform linux/amd64 -t recipe_app:v2 .

# Run the the application local on your machine
$ podman run -d --name recipe_app -p 5001:5000 localhost/recipe_app


# tag and push the image
podman tag <imageid> quay.io/rocrisp/recipe:v1
podman push quay.io/rocrisp/recipe:v1
