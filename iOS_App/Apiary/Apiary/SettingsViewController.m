//
//  SettingsViewController.m
//  Apiary
//
//  Created by John Davidge on 15/03/2014.
//  Copyright (c) 2014 John Davidge. All rights reserved.
//

#import "SettingsViewController.h"
#import "DataClass.h"

@interface SettingsViewController ()

@end

@implementation SettingsViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Get and instance of DataClass
    DataClass *obj=[DataClass getInstance];
    // Get the url and set the text field
    obj.url = [obj.data_storage objectForKey:@"URL"];
    hiveURLField.text = obj.url;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)hiveURLFieldDismiss:(id)sender {
    // Get an instance of DataClass
    DataClass *obj=[DataClass getInstance];
    // Set the URL and save it
    obj.url = hiveURLField.text;
    [obj.data_storage setValue:obj.url forKey:@"URL"];
    [obj.data_storage writeToFile:obj.filePath atomically:YES];
    // Exit the textField
    [hiveURLField resignFirstResponder];
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
