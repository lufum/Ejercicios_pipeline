# Ejercicios_pipeline
Repo de prueba para familiarizarse con git y cargar ejercicios de pipeline


Edicion
=======

git checkout -b your_branch
# Trabajamos y hacemos commits
# git add <archivo>
# o 
# git add -A
# git commit -m "Comentario descriptivo"
# Actualizar nuestra rama

# Actualizacion
git checkout master

# Actualiza todo lo que se subio a internet
git pull

# Ya actualizada la rama master
git checkout your_branch

# Juntar nuestros commits
git rebase master


# Arte ninja, jutsu estilo de fuego
git checkout master
git merge --ff-only your_branch
git push origin master

# --------------------------------------------------
# Reset local changes
git reset --hard
# Reset local changes already commited
git reset --hard HEAD
