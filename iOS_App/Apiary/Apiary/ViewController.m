//
//  ViewController.m
//  Apiary
//
//  Created by John Davidge on 10/24/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import "WebViewController.h"
#import "ViewController.h"
#import "DataClass.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    DataClass *obj=[DataClass getInstance];
    obj.url = [obj.data_storage objectForKey:@"URL"];
    obj.user = [obj.data_storage objectForKey:@"username"];
    obj.password = [obj.data_storage objectForKey:@"password"];
    obj.device_id = [obj.data_storage objectForKey:@"device_id"];
    hiveIPField.text = obj.url;
    usernameField.text = obj.user;
    passwordField.text = obj.password;
    deviceField.text = obj.device_id;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender{
    
    if (segue.identifier != NULL){
        if (!([segue.identifier isEqualToString:@"nothing"])){
            WebViewController *transferViewController = segue.destinationViewController;
    
            NSLog(@"prepareForSegue: %@", segue.identifier);
            transferViewController.request_type = segue.identifier;
        }
    }
    
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
