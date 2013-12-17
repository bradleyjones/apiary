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
    
    NSArray *directories = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documents = [directories lastObject];
    NSString *filePathURL = [documents stringByAppendingPathComponent:@"URL.plist"];
    
    DataClass *obj=[DataClass getInstance];
    obj.url = [[NSDictionary dictionaryWithContentsOfFile:filePathURL] objectForKey:@"URL"];
    hiveIPField.text = obj.url;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)hiveIPFieldDismiss:(id)sender {
    NSArray *directories = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documents = [directories lastObject];
    
    NSString *filePathURL = [documents stringByAppendingPathComponent:@"URL.plist"];
    
    NSDictionary *url_storage = @{@"URL" : hiveIPField.text};
      [url_storage writeToFile:filePathURL atomically:YES];
    
    DataClass *obj=[DataClass getInstance];
    obj.url = hiveIPField.text;
  
    [hiveIPField resignFirstResponder];
}

- (IBAction)usernameFieldDismiss:(id)sender {
    DataClass *obj=[DataClass getInstance];
    obj.user = usernameField.text;
    [usernameField resignFirstResponder];
}

- (IBAction)passwordFieldDismiss:(id)sender {
    DataClass *obj=[DataClass getInstance];
    obj.password = passwordField.text;
    [passwordField resignFirstResponder];
}
@end
