//
//  ViewController.m
//  Apiary
//
//  Created by John Davidge on 10/24/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import "ViewController.h"
#import "DataClass.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    DataClass *obj=[DataClass getInstance];
    obj.url = [[NSDictionary dictionaryWithContentsOfFile:obj.filePath] objectForKey:@"URL"];
    obj.user = [[NSDictionary dictionaryWithContentsOfFile:obj.filePath] objectForKey:@"username"];
    obj.password = [[NSDictionary dictionaryWithContentsOfFile:obj.filePath] objectForKey:@"password"];
    hiveIPField.text = obj.url;
    usernameField.text = obj.user;
    passwordField.text = obj.password;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)hiveIPFieldDismiss:(id)sender {
    DataClass *obj=[DataClass getInstance];
    obj.url = hiveIPField.text;
    [obj.data_storage setValue:obj.url forKey:@"URL"];
    
    [obj.data_storage writeToFile:obj.filePath atomically:YES];
  
    [hiveIPField resignFirstResponder];
}

- (IBAction)usernameFieldDismiss:(id)sender {
    DataClass *obj=[DataClass getInstance];
    obj.user = usernameField.text;
    [obj.data_storage setValue:obj.user forKey:@"username"];
    
    [obj.data_storage writeToFile:obj.filePath atomically:YES];
    
    [usernameField resignFirstResponder];
}

- (IBAction)passwordFieldDismiss:(id)sender {
    DataClass *obj=[DataClass getInstance];
    obj.password = passwordField.text;
    [obj.data_storage setValue:obj.password forKey:@"password"];
    
    [obj.data_storage writeToFile:obj.filePath atomically:YES];
    
    [passwordField resignFirstResponder];
}
@end
