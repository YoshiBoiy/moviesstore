# Movie Petition System - Testing Guide

## Overview
This guide walks you through testing the complete movie petition system implementation. The system allows users to create petitions for movies they want added to the catalog, and other users can vote on these petitions.

## Features Implemented

### 1. Petition Management
- **Create Petitions**: Users can create petitions for movies they want added
- **View Petitions**: All users can view active petitions
- **Search Petitions**: Search functionality by title, movie name, description, or director
- **My Petitions**: Users can view their own created petitions

### 2. Voting System
- **Vote on Petitions**: Authenticated users can vote Yes/No on petitions
- **One Vote Per User**: Each user can only vote once per petition
- **Real-time Vote Counts**: Vote counts are displayed and updated in real-time
- **Vote Status**: Users can see their voting status on each petition

### 3. User Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Bootstrap Styling**: Modern, clean interface
- **Font Awesome Icons**: Visual indicators throughout
- **AJAX Voting**: Smooth voting experience without page reloads

## Testing Steps

### Prerequisites
1. Make sure the Django server is running: `python manage.py runserver`
2. Access the application at `http://127.0.0.1:8000`

### Test Data
The system comes with pre-created test data:
- **Test Users**: testuser1, testuser2, testuser3 (password: testpass123)
- **Sample Petition**: "Add The Dark Knight to our catalog" with 2 yes votes

### Step-by-Step Testing

#### 1. Login and Navigate to Petitions
1. Go to `http://127.0.0.1:8000`
2. Click "Login" in the navigation
3. Login with username: `testuser1`, password: `testpass123`
4. Click "Petitions" in the navigation bar
5. You should see the petition list page with the sample petition

#### 2. Create a New Petition
1. While logged in as testuser1, click "Create New Petition"
2. Fill out the form:
   - **Title**: "Add Inception to our catalog"
   - **Movie Title**: "Inception"
   - **Year**: 2010
   - **Director**: "Christopher Nolan"
   - **Description**: "Inception is a mind-bending sci-fi thriller that would be perfect for our catalog. It features complex storytelling, stunning visuals, and an all-star cast."
3. Click "Create Petition"
4. You should be redirected to the petition detail page

#### 3. Test Voting (Second User)
1. Logout from testuser1
2. Login with username: `testuser2`, password: `testpass123`
3. Go to Petitions page
4. Click on the "Inception" petition you just created
5. Vote "Yes" on the petition
6. You should see the vote count update and a success message
7. Try to vote again - you should get an error message

#### 4. Test Voting (Third User)
1. Logout from testuser2
2. Login with username: `testuser3`, password: `testpass123`
3. Go to Petitions page
4. Click on the "Inception" petition
5. Vote "No" on the petition
6. You should see the vote counts update (1 Yes, 1 No, 2 Total)

#### 5. Test Search Functionality
1. While logged in as testuser3, use the search box on the petitions page
2. Search for "Inception" - should find the petition
3. Search for "Dark Knight" - should find the sample petition
4. Search for "Christopher Nolan" - should find both petitions
5. Search for "nonexistent" - should show no results

#### 6. Test My Petitions
1. While logged in as testuser1, click "My Petitions" (if available in navigation)
2. Or go directly to `http://127.0.0.1:8000/petitions/my-petitions/`
3. You should see the "Inception" petition you created
4. Logout and login as testuser2
5. Go to My Petitions - should be empty (testuser2 hasn't created any petitions)

#### 7. Test Navigation
1. Test all navigation links work correctly
2. Verify the "Petitions" link appears in the main navigation
3. Test responsive design on different screen sizes

### Expected Results

#### Petition List Page
- Shows all active petitions in a card layout
- Displays vote counts for each petition
- Shows user's vote status if they've voted
- Search functionality works
- "Create New Petition" button for authenticated users

#### Petition Detail Page
- Shows complete petition information
- Displays current vote counts
- Shows voting form for users who haven't voted
- Shows vote status for users who have voted
- Prevents duplicate voting

#### Create Petition Page
- Form validation works (minimum lengths, required fields)
- Success message after creation
- Redirects to petition detail page

#### My Petitions Page
- Shows only petitions created by the current user
- Displays vote counts
- Shows petition status (active/inactive)

### Admin Interface
1. Go to `http://127.0.0.1:8000/admin/`
2. Login with admin credentials
3. Navigate to "Petitions" section
4. You should see both Petition and Vote models
5. Test creating, editing, and managing petitions from admin

### Error Handling Tests
1. Try to vote without being logged in
2. Try to create a petition without being logged in
3. Try to vote twice on the same petition
4. Try to submit empty forms
5. Try to access non-existent petition pages

## Technical Features Demonstrated

### Database Models
- **Petition Model**: Stores petition information with proper relationships
- **Vote Model**: Stores user votes with unique constraints
- **User Integration**: Proper foreign key relationships

### Security Features
- CSRF protection on all forms
- User authentication requirements
- Input validation and sanitization
- Unique vote constraints

### User Experience
- Responsive design
- Real-time updates
- Clear feedback messages
- Intuitive navigation

## Cleanup
After testing, you can clean up test data by running:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from petitions.models import Petition, Vote
>>> User.objects.filter(username__startswith='testuser').delete()
>>> Petition.objects.all().delete()
>>> Vote.objects.all().delete()
```

## Conclusion
The petition system is now fully functional and ready for production use. Users can create petitions, vote on them, and administrators can manage the system through the Django admin interface.


