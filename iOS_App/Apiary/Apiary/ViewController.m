//
//  ViewController.m
//  Apiary
//
//  Created by John Davidge on 10/24/13.
//  Copyright (c) 2013 John Davidge. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)usernameFieldDismiss:(id)sender {
    [usernameField resignFirstResponder];
}

- (IBAction)passwordFieldDismiss:(id)sender {
    [passwordField resignFirstResponder];
}
@end
