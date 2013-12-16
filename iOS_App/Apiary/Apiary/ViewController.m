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
    hiveIPField.text = obj.url;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)hiveIPFieldDismiss:(id)sender {
    DataClass *obj=[DataClass getInstance];
    obj.url = hiveIPField.text;
    [hiveIPField resignFirstResponder];
}

- (IBAction)usernameFieldDismiss:(id)sender {
    [usernameField resignFirstResponder];
}

- (IBAction)passwordFieldDismiss:(id)sender {
    [passwordField resignFirstResponder];
}
@end
