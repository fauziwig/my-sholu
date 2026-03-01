## Development Branch
dev/electron-app branch 

## Langkah langkah Git ketika selesai develop feature 
1. Push dev branch ke github
`git push origin dev/electron-app`

2. Switch ke main branch 
`git checkout main`

3. Pull latest changes from remote (if any)
`git pull origin main`

4. Merge dev branch into main 
`git merge dev/electron-app`

5. Push updated main to Github
`git push origin main`

6. Delete dev branch if done (optional)
`git branch -d dev/electron-app`
`git push origin --delete dev/electron-app`

7. Create new dev branch for next feature (optional)
`git checkout -b dev/next-feature`





