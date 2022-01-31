# BugKiller

This is a project managment application built on AWS. It is WIP, more details will be added in the future.

(Ignore the rest of the readme)


UI:

User logs in:

-   Homepage:

    -   Search
        -   Search bar where they can search by:
            -   Projects name
            -   Details
            -   Bug name
            -   Bug details
            -   User (any team member)
    -   Actions
        -   Create project
    -   Project List
        -   Project name
        -   Count team members
        -   User assigned tasks (Goes )
        -   Actions:

-   Project Details page

    -   Name
    -   Details
    -   Members
    -   Actions
        -   Create bug
        -   Edit project
    -   Bugs List
        -   Filter options
        -   Show you ones first
        -   View details

-   Bug details
    -   Name/Details
    -   Actions
        -   Edit/Delete

Access Pattern:

-   Get all projects user is part off
-   Get project by id
-   Get project bug by PID, BID
-   Get bugs assigned to user

Table
HK SK ATTR
PID PID ... // Get project
PID BID ... // Get project bugs
PID UID ... // Get project members

LSI
PID Resolve
PID RESOLVE // Get Open bugs

GSI 1
HK SK
UID PID_BID ... // Get projects & BID user is member of
