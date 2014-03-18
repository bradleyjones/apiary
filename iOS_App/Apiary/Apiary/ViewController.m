//
//  ViewController.m
//  Apiary
//
//  Created by John Davidge on 15/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import "ViewController.h"
#import "DataClass.h"

@interface ViewController ()

@end

@implementation ViewController


- (void)viewDidLoad
{
    [super viewDidLoad];

    // Get an instance of DataClass
    DataClass *obj=[DataClass getInstance];
    // Get username and password from storage
    obj.user = [obj.data_storage objectForKey:@"username"];
    obj.password = [obj.data_storage objectForKey:@"password"];
    // Set textField properties
    usernameField.text = obj.user;
    passwordField.text = obj.password;
}

- (IBAction)usernameFieldDismiss:(id)sender {
    // Get an instance of DataClass
    DataClass *obj=[DataClass getInstance];
    // Set the username and save it
    obj.user = usernameField.text;
    [obj.data_storage setValue:obj.user forKey:@"username"];
    [obj.data_storage writeToFile:obj.filePath atomically:YES];
    // Exit the textField
    [usernameField resignFirstResponder];
}

- (IBAction)passwordFieldDismiss:(id)sender {
    // Get and instance of DataClass
    DataClass *obj=[DataClass getInstance];
    // Set the password and save it
    obj.password = passwordField.text;
    [obj.data_storage setValue:obj.password forKey:@"password"];
    [obj.data_storage writeToFile:obj.filePath atomically:YES];
    // Exit the textField
    [passwordField resignFirstResponder];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
