B4igo Api Documents
________________


List of Microservice
1. User Microservice
2. PersonalInfo Microservice
3. Health Microservice
4. Digital Microservice
5. File Microservice
6. Legal Microservice
7. Subscription Microservice
8. Notification Microservice


________________




List of User Microservice
* CreateUser: Creates a new user with personal, contact, and identity details. Returns the created user's information and status.


* TwoFAOTP: Generates and sends a two-factor authentication OTP to the user. Used for enhanced login security.


* EmailOTP: Sends an OTP to the user's email for verification purposes. Used for email validation during registration or sensitive actions.


* SetPhoneNumber: Sets or updates the user's phone number in their profile. Ensures the user's contact information is current.


* Login: Authenticates a user with credentials and returns login details. Used for user access to the system.


* UpdatePreferredName: Updates the user's preferred display name and optionally their recovery email. Helps personalize the user profile.


* MobileNumberVerification: Verifies the user's mobile number using an OTP. Confirms phone ownership for security and notifications.


* SetPassword: Sets or updates the user's password. Used for account creation or password reset flows.


* VerifyEmailOTP: Verifies the OTP sent to the user's email address. Confirms email ownership for registration or security.


* GetUserId: Retrieves the user ID based on the provided email address. Useful for account lookup and linking.


* IdTypes: Fetches the list of available ID types for user identification. Used during registration or profile updates.


* GetUserRole: Retrieves the role assigned to a user. Determines user permissions and access levels.


* GenerateQRForProxy: Generates a QR code to invite a Trusted Helper (proxy) and sends it via email/SMS. Used for secure proxy onboarding.


* ProxyReLogin: Allows a proxy user to re-login using their credentials. Supports session renewal for proxies.


* ProxyUserOptOut: Allows a proxy user to opt out and revoke their access. Used for removing proxy access.


* RevokeProxyAccess: Revokes access for a proxy user from the main user's account. Used for security and access management.


* SignUpProxy: Registers a new proxy user (Trusted Helper) for a user. Enables trusted third-party access.


* VerifyPasscode: Verifies the passcode for a proxy user. Used for authentication and security checks.


* ProxyLogin: Authenticates a proxy user and returns login details. Used for proxy access to the system.


* GetMainVaults: Fetches the main vaults accessible to a user or proxy. Used for displaying available data vaults.


* GetSubModules: Retrieves sub-modules for a given vault or user. Supports modular access and navigation.


* GetProxyUserMessage: Fetches messages or notifications for a proxy user. Used for communication and alerts.


* GetNationality: Retrieves the list of available nationalities. Used during registration or profile updates.


* ContactUs: Submits a contact or support request from the user. Used for customer support and inquiries.


* ThanksForRegisteringQR: Generates a "Thank You for Registering" QR code for the user. Used for onboarding and engagement.


* SignUpSubscriber: Registers a new subscriber user for a main user. Captures identity and contact details for sharing.


* VerifySubscriberPasscode: Verifies the passcode for a subscriber user. Used for authentication and access control.


* RevokeSubscriberAccess: Revokes access for a subscriber user. Used for removing shared access.


* GetDID: Fetches the Decentralized Identifier (DID) for a user or subscriber. Used for decentralized identity management.


* SubscriberOptOut: Allows a subscriber user to opt out and revoke their access. Used for access management and compliance.


* GetAccessEventDropdown: Fetches the list of available access events for subscribers. Used for configuring sharing events.


* GetSubscriberAccessTypes: Retrieves available access types for subscribers. Supports granular access control.


* AssignSubscriber: Assigns a subscriber to a user and shares selected vaults/modules. Used for controlled data sharing.


* SubscriberLogin: Authenticates a subscriber user and returns login details. Used for subscriber access to the system.


* GetUserDetails: Fetches detailed information about a subscriber user. Used for profile and access management.


* CheckAssigne: Checks if a subscriber is assigned to a user. Used for validation before sharing or revoking access.


* TransferOwnership: Transfers ownership of a record or vault to another user. Used for data and responsibility transfer.


* GetB4igoProfile: Fetches the B4igo profile for a user or subscriber. Used for displaying and managing user profiles.


* UpdateB4igoProfile: Updates the B4igo profile for a user or subscriber. Used for profile management.


* SetProfilePicture: Sets or updates the profile picture for a user or subscriber. Used for personalizing the profile.


* DeleteProfilePicture: Deletes the profile picture for a user or subscriber. Used for profile management.


* GetProfilePicture: Fetches the profile picture for a user or subscriber. Used for displaying user avatars.


* GetSharedInfo: Retrieves shared information for a user or subscriber. Used for access and sharing management.


* RemoveModuleAccess: Removes access to a module for a user or subscriber. Used for granular access control.


* RejectModuleAccess: Rejects access to a module for a user or subscriber. Used for access management.


* RejectSubModuleAccess: Rejects access to a sub-module for a user or subscriber. Used for detailed access control.


* GetUnsharedVaults: Fetches the list of vaults not yet shared with a subscriber. Used for sharing management.


* GetVisionDetailsList: Retrieves the list of vision details for a user or subscriber. Used for managing vision-related data.


* refreshToken: Generates a new access and refresh token for a user, given a valid refresh token. Used for session renewal.


* confirmInitiateVoting: Confirms the initiation of a voting process for a user or subscriber. Used in voting workflows.


* actionForVoting: Performs an action (approve/reject) for a voting event. Used to record voting decisions.


* GetSubscriberVoting: Fetches voting details for a subscriber. Used to display voting status and history.


* HelloServer: Performs a server handshake for SIWE (Sign-In With Ethereum) authentication. Used for blockchain-based login.


* VerifySignature: Verifies a cryptographic signature for SIWE authentication. Ensures authenticity of blockchain logins.


* StoreVC: Stores a Verifiable Credential (VC) for a user. Used for decentralized identity and credential management. Data.


* FetchEncryptedBlob: Fetches an encrypted data blob for a user. Used for retrieving securely stored data.










* ResendOtp: Resends an OTP to the user. Used for authentication and verification.


* GetFilters: Fetches available filters for user data. Used for search and filtering.


* GetSharedModulesForPersona: Fetches shared modules for a specific persona. Used for access and sharing.


* DaoBoolean: Performs a DAO boolean operation for a user. Used for DAO-related workflows.


* UserSubscriptionInvoice: Fetches the subscription invoice for a user. Used for billing and subscription management.


* RevokeProxyAccessNew: Revokes proxy access for a user. Used for access management.
* RevokeCustodian: Revokes a custodian for a user. Used for custodian management.


* EditProxyNew: Edits proxy details for a user. Used for updating proxy information.


* EditCustodianNew: Edits custodian details for a user. Used for updating custodian information.


* CancelVaultAccess: Cancels vault access for a user. Used for access management.


* CheckSubscriber: Checks subscriber details for a user. Used for validation and management.


* CheckTrustedHelp: Checks trusted helper details for a user. Used for validation and management.




________________




List of PersonalInfo Microservice
Query:
* getRelationshipStatus: Fetches a paginated list of relationship status records for a user.
* getRelationshipStatusById: Fetches a single relationship status record by its ID and user ID.
* relationshipStatusDropDown: Fetches a dropdown list of available relationship statuses for a given user.
* getIdentityProofById: Fetches a specific identity proof record for a user by its ID.
* getAllIdentityProofs: Fetches all identity proof records for a given user.
* getDependentTypes: Fetches the list of available dependent types (e.g., child, spouse, parent) for use in forms or profile management.
* getDependentDetailsById: Fetches the details of a specific dependent for a user by dependent ID.
* getAllDependentDetails: Fetches all dependent records for a given user.
* getIdentityProofTypes: Fetches all dependent records for a given user
* getAddressTypes: Fetches the list of available address types (e.g., Home, ffice) for use in address forms.
* GetAddressDetailsById: Fetches detailed address information for a specific address record by its ID and userId.
* GetAllAddressDetails: Fetches a paginated list of all address records for a user, including detailed information and associated files.
* getEducationByUserId: Fetches a paginated list of all education records for a user, including detailed information and associated files.
* getEducationById: Fetches a single education record for a user by its ID and userId, including all details and associated files.
* getSkillSets: Fetches the list of available skill sets in the system.
* getContactByUserId: Fetches a paginated list of contact details for a user, with filtering options.
* getContactById: Fetches a single contact record for a user by its ID and userId, including all details.
* getContactType: Fetches the list of available contact types in the system.
* getRelationTypes: Fetches the list of available relation types in the system.
* getSalaryRange: Fetches the list of available salary ranges.
* getEmploymentType: Fetches the list of available employment types.
* getTypefEmployment: Fetches the list of available types of employment.
* getEmploymentById: Fetches a specific employment record by its ID and user ID.
* getAllEmployment: Fetches a paginated list of all employment records for a user.
* getDashboard: Fetches dashboard progress and completion status for a user's vault, including submodules and their completion metrics
* getAddressDependentsByUserId: Fetches a list of address dependents for a user, optionally filtered by current relation status.
* getAddressDependentsById: Fetches the dependents related to a specific address for a given user by their ID.
* printPdf: Generates and returns PDF-related data for a user, including identity proofs and address details, based on provided module IDs and vault ID.
* emergencyContactBreclate: Fetch the contact bracelet by user Id
* getIndustries: Fetches the list of available industries.
* getSubCategories: Fetches the list of subcategories for a given industry.
* getCertificationStatuses: Fetches the list of available certification statuses.
* getProficiencyLevels: Fetches the list of available certification statuses.


Mutation:
*  createRelationshipStatus: Creates a new relationship status record for a user.
* updateRelationshipStatus: Updates an existing relationship status record for a user
* deleteRelationshipStatus: Deletes a relationship status record for a user.
* addIdentityProof: Add a new identity proof record for a user
* updateIdentityProof: Updates an existing identity proof record for a user, including document details and file uploads.
* deleteIdentityProof: Deletes an identity proof record for a user.
* addDependent: Adds a new dependent record for a user.
* deleteDependent: Deletes a dependent record for a user.
* updateDependent: Updates an existing dependent record for a user.
* addAddressDetails: Adds a new address record for a user, including address details and optional file uploads.
* updateAddressDetails :Updates an existing address record for a user, including address details and optional file uploads.
* deleteAddressDetails: Deletes an address record for a user by its unique ID.
* createEducation: Creates a new education record for a user.
* updateEducation: Updates an existing education record for a user.
* deleteEducationById: Deletes an education record for a user by its unique ID.
* createContact: Creates a new contact record for a user.
* updateContact: Updates an existing contact record for a user.
* deleteContact: Delete one or more contact records for a user by their IDs.
* addEmployment: Add a new employment record for a user, including company, designation, employment type, salary range, address, tes, and supporting files.
* updateEmployment: Update an existing employment record for a user, including company, designation, employment type, salary range, address, tes, and supporting files.
* deleteEmployment: Delete an employment record for a user by its ID.
* addRelationAndDependents: Add one or more relation and dependent records for a user, including address, relation/dependent details, files, and metadata.
* updateRelationAndDependents: Update one or more relation and dependent records for a user, including address, relation/dependent details, files, and metadata.
* deleteFilesRD: Delete a file associated with a relation or dependent record for a user.
* deleteRelationDependents: Delete a relation or dependent record by its ID.
* deleteRelationDependentsById: Deletes a specific relation or dependent record by its ID, user ID, and type.
* fileReUpload: mutation is to allow a user to re-upload or replace an existing file associated with a record
* addSkillSets: mutation is to allow users to add multiple skill sets, organized by industry and category, to their profile. It enables bulk creation of skills, including details like proficiency, certification, experience, and associated files, helping users comprehensively manage and update their professional skill information.
* deleteSkillSet: mutation is to allow a user to remove a specific skill from their profile, identified by user, industry, category, and skill IDs. This helps users manage and update their skill records by deleting outdated or incorrect skill entries.


________________


List of Health Microservice
* GetAllDoctors :- Retrieves a list of doctors associated with a user. Supports GraphQL queries for field selection.
* UpdateCountry :- Updates the country name for the specified country ID.
* DeleteCountry :- Delete a country from the database of specified country ID if no form locations are associated with its country ID.
* CreateCountry :- Creates a new country.
* AddQuestion :- Inserts new questions into the database for a given form.
* DeleteState :-  Deletes a state by its ID.
* GetForms :- Fetches a list of all forms values.
* UpdateQuestion :-  Update the question data for the specified question ID
* CreateForm :-  Creates a new form.
* DeleteQuestion :- Delete the question data for the given question ID and delete all associated form questions.
* AddState :- Add new state into database
* UpdateForm :- Update the form data for the specified form ID
* UserAhdForm :- Fetches form data for a given form ID, including all questions and their corresponding answers.
* GetStates :- Fetches a list of all state data.
* GetForm :- Retrieves the form details based on countryId and stateId from the database.
* CreateMedicalHistory :- Stores a user's medical history record and uploads associated documents to the server.
* CreateFamilyDoctor :- Adds a new family doctor record for a user, including doctor details and contact information.
* CreateMedicationAllergy :- Inserts a medication or allergy record for a user and uploads any related files.
* CreateNote :-  Creates a new note for a user, optionally attaching files to the note.
* CreateHealthInsurance :- Adds a health insurance record for a user, including member details and uploads related documents.




* UpdateCountry: Updates the details of a country for a user. Used to maintain accurate country information in the user’s health profile.
* DeleteCountry: Deletes a country record for a user. Removes country data that is no longer relevant to the user’s account.
* CreateCountry: Creates a new country record for a user. Adds country information to support user health data localization.
* AddQuestion: Adds a question to a form or section. Enables customization of health forms with user-specific questions.
* DeleteState: Deletes a state record for a user. Removes state data from the user’s health profile when no longer needed.
* UpdateQuestion: Updates a question in a form or section. Allows modification of existing questions for improved data collection.
* CreateForm: Creates a new health form for a user. Supports the creation of custom forms for health data entry.
* DeleteQuestion: Deletes a question from a form or section. Cleans up forms by removing outdated or unnecessary questions.
* AddState: Adds a new state record for a user. Enhances user profiles with relevant state information.
* UpdateForm: Updates an existing health form for a user. Enables changes to form structure or content for better usability.
* UserAhdForm: Fetches the Advance Health Directive form for a user. Provides access to user-specific AHD data for review or editing.
* CreateMedicalHistory: Creates a new medical history record for a user. Stores important health events and conditions in the user profile.
* CreateFamilyDoctor: Adds a family doctor record for a user. Links the user to their primary healthcare provider.
* CreateMedicationAllergy: Creates a new medication allergy record for a user. Documents allergies for safer medication management.
* CreateNote: Adds a note to the user’s health profile. Allows users to record personal health observations or reminders.
* CreateHealthInsurance: Creates a new health insurance record for a user. Stores insurance details for coverage verification and claims.
* UpdateState: Updates the details of a state for a user. Keeps state information current in the user’s health profile.
* DeleteForm: Deletes a health form for a user. Removes forms that are obsolete or no longer required.
* DeleteMedicalHistory: Deletes a medical history record for a user. Cleans up outdated health event data.
* DeleteDoctorDetails: Deletes a doctor details record for a user. Removes provider information that is no longer relevant.
* DeleteHealthInsurance: Deletes a health insurance record for a user. Removes insurance data when coverage changes.
* DeleteMedicationAndAllergies: Deletes medication and allergy records for a user. Ensures only current health data is retained.
* SubmitAhdForm: Submits an Advance Health Directive form for a user. Finalizes and saves the user’s AHD responses.
* UpdateNotes: Updates a note in the user’s health profile. Allows users to revise personal health observations.
* UpdateFamilyDoctor: Updates family doctor details for a user. Keeps provider information accurate and up to date.
* UpdateMedicationAndAllergies: Updates medication and allergy details for a user. Ensures health records reflect current conditions.
* DeleteNote: Deletes a note from the user’s health profile. Removes notes that are no longer needed.
* UpdateHealthInsurance: Updates health insurance details for a user. Maintains accurate insurance coverage information.
* CreateAllergy: Adds a new allergy record for a user. Documents allergies for improved health safety.
* DeleteAllergyDetails: Deletes an allergy record for a user. Removes outdated allergy information.
* UpdateAllergies: Updates allergy details for a user. Keeps allergy records current for better care.
* CreateMeicalHistoryV2: Creates a new version of medical history for a user. Stores updated health event data.
* UpdateMedicalHistory: Updates medical history details for a user. Ensures health records are accurate and complete.
* AddQuestionsToSection: Adds questions to a section in a health form. Customizes sections for targeted data collection.
* UpdateQuestionsToSection: Updates questions in a section of a health form. Refines section content for better responses.
* DeleteQuestionFromSection: Deletes a question from a section in a health form. Removes unnecessary questions for clarity.
* SubmitAhdFormV2: Submits an updated Advance Health Directive form for a user. Saves new AHD responses and details.
* DeleteAHDForm: Deletes an Advance Health Directive form for a user. Removes AHD data that is no longer needed.
* SetAHDPersonalDetails: Sets or updates personal details for Advance Health Directive. Ensures user identity and contact info are current.
* SubmitAhdFormV3: Submits the latest version of the Advance Health Directive form. Includes advanced features like witness and QR code.
* AddAhdContacts: Adds new contacts to the user’s AHD profile. Supports emergency and trusted contact management.
* UpdateAhdContacts: Updates contact details in the user’s AHD profile. Keeps contact information accurate.
* ListAllAhdContacts: Lists all contacts in the user’s AHD profile. Provides a complete view of emergency and trusted contacts.
* DeleteAhdContact: Deletes a contact from the user’s AHD profile. Removes contacts that are no longer relevant.
* WitnessSignUp: Registers a witness for an AHD form. Supports legal validation of the user’s health directive.
* WitnessConsent: Records consent from a witness for an AHD form. Confirms witness agreement for legal compliance.
* ResetAHDForm: Resets the user’s Advance Health Directive form. Allows users to start over or clear previous responses.
* SeverityDropDown: Fetches severity dropdown options for forms. Provides standardized severity levels for health data.
* AddAgentWitness: Adds an agent witness for a user’s health directive. Supports proxy and agent validation.
* MedicalAgentSignUp: Registers a medical agent for a user. Enables agent access and management of health directives.
* CombinedLogin: Authenticates a user or agent with combined credentials. Supports secure access for multiple roles.
* VerifyAhdPasscode: Verifies the AHD passcode for a user or agent. Confirms identity for secure form access.
* DeleteHealthFiles: Deletes health files from the user’s profile. Removes outdated or unnecessary documents.
* HealthFileReupload: Reuploads a health file for a user. Updates file data for accuracy and completeness.
* PrintPdfHealth: Generates a PDF of the user’s health data. Supports sharing and printing of health records.
* AddHealthCareAccount: Adds a health care account for a user. Stores account details for health service access.
* UpdateHealthCareAccount: Updates health care account details for a user. Maintains current account information.
* DeleteHealthCareAccount: Deletes a health care account for a user. Removes accounts that are no longer active.
* AddSupplement: Adds a supplement record for a user. Documents supplement usage for health tracking.
* UpdateSupplement: Updates supplement details for a user. Keeps supplement records accurate and current.
* DeleteSupplement: Deletes a supplement record for a user. Removes supplements that are no longer used.
* ServeHealthVaultFile: Serves a health vault file for a user. Provides access to stored health documents.
* AddMymedicalRecord: Adds a medical record to the user’s profile. Supports comprehensive health documentation.
* UpdateMymedicalRecord: Updates a medical record for a user. Ensures medical records reflect current information.
* updateMedicalAgeBloodGroup: Updates age and blood group for a user. Maintains demographic health data.
* EmergencyAlert: Fetches age and blood group for emergency alerts. Supports rapid response in emergencies.
* updateEmergencyAlert: Updates emergency alert details for a user. Ensures alert information is current.
* BraceletAhd: Fetches AHD details for bracelet integration. Supports wearable device access to health directives.
* SubmitConsentConfirmationHealth: Submits consent confirmation for health POA. Records legal agreement for proxy access.
* ResendPersonaOtpHealth: Resends OTP for persona verification. Supports secure identity confirmation.
* RevokeByRole: Revokes access by role for a user. Manages permissions for agents and witnesses.
* RejectHealthModuleAccess: Rejects access to a health module for a user. Denies module permissions for security.
* rejectHealthPoaModuleAccess: Rejects access to a health POA module for a user. Denies POA permissions for security.




List of Health Microservice(Queries)
* countries:Returns a list of all countries available in the system. Includes metadata such as message, status code, and success flag.
* Country: Retrieves details of a specific country using its ID. Returns country information along with response metadata.
* states: Returns a list of states that belong to the specified country ID. The response includes a status code, success flag, and an array of state data.
* state: Fetches details of a specific state based on its unique state ID. Response includes full state information and operation metadata.
* forms: Retrieves a list of all available forms in the system, including metadata and basic details.
* form: Fetches a specific form based on a given country ID and state ID.
* responses: Returns all responses submitted for a specific form ID.
* response: Fetches detailed information of a single form response based on its ID.
* getAllMedicalHistory: Retrieves the entire medical history records for the given user ID.
* getAllDoctors: Returns a list of all doctors added by the user based on their user ID.
* getInsuranceById: Fetches health insurance details by insurance ID and user ID.
* getTypeOfHealthInsurance: Returns a list of all available health insurance types in the system.
* getTypeOfDoctor: Retrieves all defined doctor types (e.g., general, specialist) used in the system.
* userAhdForm: Fetches AHD (Advance Healthcare Directive) form responses for a specific user and form ID with pagination.
* getUserMedicalHistory: Fetches details of a specific medical history entry based on its ID.
* getDoctorById: Retrieves information about a specific doctor by their doctor ID and user ID.
* getHealthInsurancesByUserId: Returns all health insurance entries associated with a given user.
* getMedicationsByUserId: Retrieves all medication records for a user with optional pagination.
* getNotesByUserId: Fetches all notes associated with a specific user ID.
* getNotesById: Returns a particular note by note ID and user ID.
* getMedicationById: Retrieves a single medication entry based on its ID and user ID.
* getAllergy: Returns detailed information for a specific allergy ID and user ID.
* getAllergiesByUserId: Fetches all allergy records linked to a specific user with optional pagination.
* getTypeOfAllergies: Returns the list of all predefined allergy types in the system.
* getBloodGroup: Retrieves all possible blood group types used in the platform.
* getRelationship: Returns the list of relationship types (e.g., sibling, spouse, parent).
* getUserMedicalResponses: Fetches medical responses submitted by a user for a specific section ID.
* getUserMedicalAndEmergencyResponses: Returns combined medical and emergency responses for a specific user and section.

* getFamilyMedicalHistoryResponses: Fetches family medical history responses for a given user and section.
* getAllQuestionsFromSection: Retrieves all questions defined under a specific section.
* getSections: Returns the list of all available sections configured for a user.
* getFilledSections: Fetches the sections already filled/submitted by a user.
* getSubmittedSection: Returns detailed information about a specific submitted section based on user input.
* GetHealthprogressbar: Fetches progress bar details to indicate completion of medical information sections.
* getStates: Returns a list of states that exist in the system.
* listAllAhdContacts: Lists all AHD (Advance Healthcare Directive) contacts associated with the user.
* getSeverity: Returns available severity levels used in medical responses.
* getSelectedSections: Fetches the list of medical sections selected by the user.
* printPdfHealth: Generates a PDF version of the user's health data based on specified input.
* getMedicalUserResponseById: Returns a single medical user response using user ID and response ID.
* getMyMedicalPoa: Retrieves the user's Medical Power of Attorney details.
* getHealthAccByUserId: Fetches all health account credentials (e.g., portal logins) stored by a user.
* getHealthAccById: Returns details of a specific health account entry using its ID and user ID.
* getSupplements: Fetches all supplement entries associated with a user.
* getSupplementByID: Returns details of a specific supplement by ID.
GetAllHealthVaultFiles: Retrieves all files uploaded by a user under their health vault.
* getMedicalAgeBloodGroupSingle: Returns user’s age and blood group based on the user ID.
* emergencyAlert: Fetches emergency alert data for a user, including diseases and associated information.
* braceletAhd: Returns emergency contact and AHD-related contact information for display on a medical bracelet.
* getHealthVaultFiles: Retrieves a specific file from the health vault based on input filters.
* getAgentWitnessDetails: Returns agent or witness details based on provided ID and type (used in legal/POA contexts).
List of Digital Microservice:
   * GetSocialMediaRecords:Fetches a list of social media records for a user based on userId and queries the database to fetch the records for the user.
   * CreateOrUpdateSocialMediaEntry: Creates or updates a social media entry for a user.Based on the unique ID of users it creates or updates record in database
   * DeleteSocialMediaRecord: Deletes a social media record for a user from database which is selected from UI to delete.
   * GetSocialMediaRecordById: Fetches a specific social media record by its ID.Fetches the selected Social media record on UI. 
   * getPrivateFolderTypes: Fetches all private folder types.
   * createPrivateFolder: Creates a new private folder for a user.
   * getPrivateFolderByUserId: Fetches all private folders for a user.And makes use of pagination to properly display the records on each page with count.
   * deletePrivateFolder: Deletes a private folder for a user.Whenever user selects a private folder to  be deleted this API comes into picture.
   * updatePrivateFolder: Updates an existing private folder for a user.This API comes into picture when the user wants to update a private folder.
   * getPrivateFolderById: Fetches a specific private folder by its ID.Based on the ID passed by the frontend it fetches the private folder.
   * GetManageDevicesRecords: Fetches a list of device records for a user with pagination.Based on the request it fetches the manage device records and makes use of pagination to properly display it on the UI.
   * CreateOrUpdateManageDevices: Creates or updates a manage  device record for a user.
   * DeleteManageDevicesRecordbyID: Deletes a specific device record by its ID.This API comes into picture when you want to delete a specific Manage Devices record from the Database.
   * GetManageDevicesByUserId: Fetches all device records for a user.Based on user ID this API fetches all devices related to that particular UserID.
   * GetManageDevicesById: Fetches a specific device record by its ID.
   * DeleteManageDevices: Deletes all device records for a user.This API is used when we want to delete all device records from the system.
   * GetAccessTypes: Fetches all access types for a user.This API simply fetches the Access Type for a user.
   * GetEmailPurpose: Fetches all email purposes.
   * GetEmailAccounts: Fetches a list of email accounts for a user with pagination.
   * AddEmailAccount: Creates a new email account entry for a user.This API is used to simply add Email Accounts into the system.
   * DeleteEmailAccount: Deletes a specific email account by its ID.
   * GetEmailAccountById: Fetches a specific email account by its ID.
   * GetSocialMediaServiceTypes: Fetches all social media service types.
   * DeleteEmailFile: Deletes a specific file associated with an email account.
   * GetServiceNames: Fetches all service names.
   * GetSubscriptions: Fetches a list of subscriptions for a user with pagination.This API is used to fetch the list of subscription plans available in the system.
   * GetSubscriptionByID: Fetches a specific subscription by its ID.
   * UpdateSubscription: Updates an existing subscription for a user.
   * CreateSubscription: Creates a new subscription for a user.
   * DeleteSubscription: Deletes a specific subscription by its ID.
   * DeleteFilesDm: Deletes a specific file associated with a digital vault module.
   * DigitalFileReupload: Reuploads a file to a specific digital vault module.
   * GetDigitalDashboardProgress: Fetches the progress of digital vault modules for a user.
   * PrintPdfDigital: Generates a PDF report for digital vault data based on specified modules.
   * KeyMasterPrintPdf: Generates a PDF report for key master data based on specified modules.
   * GetDigitalDataBasedOnType: Fetches digital vault data based on the specified type and filters.
   * GetOtherAccounts: Fetches all "other" accounts for a user.
   * GetOtherAccountID: Fetches a specific "other" account by its ID.
   * UpdateOtherAcc: Updates an existing "other" account.
   * DeleteOtherAcc: Deletes a specific "other" account.
   * SetCredentialPair: Sets a credential pair for a user.
   * GetCredentialPair: Retrieves a credential pair by its path hash.
   * DeleteCredentialPair: Deletes a credential pair by its path hash.
________________




List of File Mircoservice:
   * Upload :- Uploads a file to a specified bucket and folder in GCS (Google Cloud Storage). 
   * Fetch :- Fetches a file from a specified bucket in GCS (Google Cloud Storage). 


________________


List of LegalVault Microservice: 
Query 
   *  legalVault  :- Check if the legal vault is enabled using a boolean value. 
   *  getAllLastWills  :- Fetch a user's last wills based on their user ID. 
   *  getLastWillByID  :- Fetch a specific last will using its ID and user ID. 
   * getAssetType/getHomeType/getUtilityType   :- Retrieve all available asset types. 


Mutation: 
   *  addLastWill  : Add a new last will record. 
   *  updateLastWill  : Update an existing last will record. 
   * deleteLastWill  : Delete a last will record by ID. 
   * addProperty  : Add a new property record. 
   * updateProperty  : Update an existing property record. 


 List of Subscription Microservice: 
Query
   * listSubscriptions :- Fetch a user subscription history and their currently active subscription plan based on the given userId.
   * getPricingPlans :- Fetch all available subscription pricing plans.
   * listCurrentPlan :- Fetch the current active plan details based on the userId.
   * getTenure :- Returns all the subscription tenure plans available in the portal (like monthly, yearly, lifetime plans, etc.).
   * getPlanFeatures: Fetches all plan features based on the main vault configuration and returns the associated vault groups and modules corresponding to the provided vault ID.
   * getPriceComparison: Returns a comparison of all available subscription plans, including their pricing for different durations and any applicable discounts.
   * listCoupons: Provides a list of all coupons available to a user, including their details, usage limits, and validity periods, enabling users to view and select applicable discounts.
   * discountAmount: query provides the original amount, the amount after discount, and a message about the discount for a specific plan and tenure, helping users see the effective price after discounts.
   * getPlan: query is used to check if a specific plan or submodule exists or is valid, returning a boolean status. Both arguments are optional, allowing for flexible checks.
   * getSubscriptionInvoice: query provides a detailed invoice for a user's subscription, including all relevant billing, plan, and payment details.
Mutation:
   * cancelSubscription: This mutation allows an authenticated user to cancel a subscription, returning the status, message, and any error details
   * proceedToCheckOut: Initiates the checkout process for a user purchasing a subscription plan, returning a session ID for payment processing.
   * addCoupon: Mutation allows an authenticated user to add a new coupon, specifying all relevant details including code, type, discount, validity, and usage limits.
   * applyCoupon: mutation checks and applies a coupon for a user’s order, returning the discount, coupon code, and related details.


List of Notification Microservice


Query
   * notificationStream: Subscribes to a real-time stream of notifications for a given user based on userID and optional filter. Returns the full notification response including unread counts and data.
Mutation:
   * createNotification: Creates a new notification with detailed input including sender, recipient, content, type, and related record IDs or modules.
   * readNotification: Marks a specific notification as read for a user, requiring userId and notificationId.
   * updateApproveStatus: Updates the approval status (e.g., Approved, Rejected, Pending) for a notification, based on Id, userId, and the new ApproveStatus.
________________


API LIST


API: GetAllDoctors
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	The ID of the user whose doctors need to be fetched.
	

🔸 Response Fields (doctor array)


Field
	Type
	Required
	Description
	doctorId
	Int
	✅
	Unique identifier of the doctor.
	userId
	String
	✅
	ID of the user associated with the doctor.
	typeId
	Int
	✅
	Doctor's type ID.
	typeName
	String
	✅
	Name of the doctor’s type.
	doctorName
	String
	✅
	Full name of the doctor.
	contactInformation
	String
	

	Phone number or other contact info.
	city
	String
	

	City of the doctor.
	state
	String
	

	State of the doctor.
	country
	String
	

	Country of the doctor.
	markAsImportant
	Boolean
	

	Whether the doctor is marked as important.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedAt
	String
	✅
	Timestamp of the last update.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	













API: proxyQRCode
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user assigning proxy access.
	hours
	Int
	✅
	Number of hours the proxy QR code remains valid.
	minutes
	Int
	✅
	Number of minutes added to expiry (used with hours).
	personalMessage
	String
	✅
	Custom message displayed with the QR code.
	isPresent
	Boolean
	✅
	Whether the trusted helper is currently present in person.
	trustedHelperName
	String
	✅
	Name of the trusted helper.
	phoneNumber
	String
	✅
	Contact number of the trusted helper.
	emailId
	String
	✅
	Email address of the trusted helper.
	sharedVaults
	Array<Int>
	✅
	List of vault IDs to which access will be granted.
	🔸 Response Fields
Field
	Type
	Required
	Description
	message
	String
	   ✅
	Human-readable message indicating the outcome of the operation.
	success
	Boolean
	   ✅
	true if the QR code was generated successfully.
	code
	Int
	    ✅
	Status code (e.g. 200 for success).
	error
	String
	

	Error message if the request failed; null on success.
	qr
	String
	     ✅
	Base64-encoded QR code image string.
	qrLink
	String
	                      ✅
	URL link to download or view the generated QR code.
	

API: UpdateCountry
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user updating country.
	id
	String
	✅
	Country ID to update
	name
	String
	✅
	New country name
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the country was updated successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: DeleteCountry
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user deleting the country.
	id
	String
	✅
	Country ID to delete
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the country was deleted successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: CreateCountry
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	

	ID of the user creating the country
	name
	String
	✅
	Country name
	created_by
	String
	✅
	ID of the user creating the country
	updated_by
	String
	

	ID of the user updating the country
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the country was created successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: AddQuestion
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	

	ID of the user creating the questions
	form_id
	String
	✅
	ID of the Form question
	created_by
	String
	✅
	ID of the user creating the questions
	updated_by
	String
	

	ID of the user updating the questions
	questions
	[QuestionInput]
	✅


	List of questions
	🔹 Nested Type: QuestionInput
Field
	Type
	Required
	Description
	question_text
	String
	✅


	A string containing the text content of the question displayed in the form.
	question_type
	String
	✅
	A string specifying the type of question (e.g., multiple-choice, text input).
	is_Required
	Boolean
	✅
	A boolean indicating whether the question must be answered (true for Required, false for optional).
	position
	Int
	✅


	An integer representing the order or ID of the question in the form.
	question_options
	[String]
	

	An array of strings listing the possible answer choices for the question.
	



🔸 Response Fields
Field
	Type
	Required
	Description
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	

API: DeleteState
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	

	ID of the user deleting the state
	id
	Int
	✅
	State ID to delete
	country_id
	Int
	✅
	Country id associated with this state
	updated_by
	String
	

	ID of the user deleting the state
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the state was deleted successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: GetForms
🔸 Request Payload
Field
	Type
	Required
	Description
	

	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the form value was retrieved successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	forms
	[Forms]
	

	List of form values
	🔹 Nested Type: Forms
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the form.
	title
	String
	✅
	Title of the form
	description
	String
	

	Description of the form
	createdAt
	String
	✅
	Timestamp of when the record was created.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	





API: UpdateQuestion
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who updates the entry.
	id
	Int
	✅
	ID of the question
	text
	String
	✅
	A new string containing the text content of the question displayed in the form.
	type
	String
	

	A string specifying the new type of question.
	isRequired
	Boolean
	✅
	A boolean value indicating whether the question must be answered (true for Required, false for optional)
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the question was updated successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: CreateForm
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who created the entry.
	title
	String
	✅
	Title of the form.
	description
	String
	

	Description of the form's value.
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the form was created successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: DeleteQuestion
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	

	ID of the user who deleted the entry.
	id
	Int
	✅
	Question ID to delete
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the question was deleted successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: AddState
🔸 Request Payload
Field
	Type
	Required
	Description
	countryId
	Int
	

	The ID of the country associated with the state.
	stateName
	String
	✅
	The name of the state.
	userId
	String
	✅
	The ID of the user who created the entry
	



🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	

	HTTP status code
	success
	Boolean
	

	true if the state was created successfully.
	message
	String
	

	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	

API: UpdateForm
🔸 Request Payload
Field
	Type
	Required
	Description
	title
	String
	✅
	New title of form
	description
	String
	✅
	New description of the form's value.
	updatedBy
	String
	

	ID of the user who last updated the entry.
	userId
	String
	✅
	The ID of the user who updated the entry
	id
	Int
	✅
	ID of the form to update
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	

	HTTP status code
	success
	Boolean
	

	true if the form was updated successfully.
	message
	String
	

	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	API: UserAhdForm
🔸 Request Payload
Field
	Type
	Required
	Description
	formId
	Int
	✅
	The unique identifier for the form.
	userId
	String
	✅
	The ID of the user whose form response was retrieved.
	page
	Int
	

	The page number for paginated results.
	limit
	String
	

	The maximum number of entries to return per page.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	ahdform
	[AhdForm]
	

	List of AHD form
	🔹 Nested Type: AhdForm
Field
	Type
	Required
	Description
	title
	String
	✅
	

	description
	String
	✅
	

	submittedAt
	String
	✅
	Timestamp of when the record was created.
	questions
	[Question]
	✅
	List of question
	

🔹 Nested Type: Question
Field
	Type
	Required
	Description
	title
	String
	✅
	

	description
	String
	✅
	

	submittedAt
	String
	✅
	

	questions
	[Question]
	✅
	

	

API: GetStates
🔸 Request Payload
Field
	Type
	Required
	Description
	countryId
	Int
	✅
	The unique identifier of a country.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	

	HTTP status code
	success
	Boolean
	

	true if the states are retrieved successfully.
	message
	String
	

	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	states
	[State]
	

	List of state
	🔹 Nested Type: State
Field
	Type
	Required
	Description
	stateId
	Int
	✅
	Unique identifier of the state.
	stateName
	String
	✅
	Name of the state
	createdAt
	String
	✅
	Timestamp of when the record was created.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	status
	Boolean
	

	Status of the state
	

API: GetForm
🔸 Request Payload
Field
	Type
	Required
	Description
	countryId
	Int
	✅
	The unique identifier of a country.
	stateId
	Int
	✅
	The unique identifier of a state.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the form detail was retrieved successfully.
	message
	String
	✅
	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	form
	[GetForm]
	✅


	List of form details
	🔹 Nested Type: GetForm
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the form.
	title
	String
	✅
	Title of the form
	description
	String
	✅
	Description of the form
	createdAt
	String
	✅
	Timestamp of when the record was created
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	status
	Boolean
	

	Status of the form
	questions
	[GetQuestion]
	✅
	List of question associated with this form
	🔹 Nested Type: GetQuestion
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the question.
	questionText
	String
	✅
	A string containing the text content of the question displayed in the form.
	questionType
	String
	✅
	A string specifying the type of question.
	isRequired
	Boolean
	✅
	A boolean indicating whether the question must be answered (true for Required, false for optional).
	createdAt
	String
	✅
	Timestamp of when the record was created.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	status
	Boolean
	

	Status of the question
	options
	[QuestionOption]
	✅
	List of options associated with this question.
	🔹 Nested Type: QuestionOption
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the question option.
	optionText
	String
	✅
	Title of the question option
	questionId
	String
	✅
	Question ID which is associated with this Question option
	

API: CreateMedicalHistory
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who created the entry.
	typeOfRecordId
	Int
	✅
	The unique identifier of type of record.
	recordDate
	String
	✅
	Timestamp of when the record was created.
	createdBy
	String
	✅
	ID of the user who created the entry.
	files
	[File]
	✅
	List of file
	🔹 Nested Type: File
Field
	Type
	Required
	Description
	file
	Byte
	✅
	Unique identifier of the question.
	originalFilename
	String
	✅
	A string containing the text content of the question displayed in the form.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅
	true if the medical history was created successfully.
	message
	String
	✅


	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	id
	Int
	



	Newly create ID of the medical history
	recordIdentifier
	String
	

	Unique UUID for traceability.
	API: CreateFamilyDoctor
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who created the entry.
	typeId
	Int
	✅
	Unique identifier for the doctor type.
	typeName
	String
	✅


	Name of the doctor type. If "Others" is selected, specify the custom doctor type.
	doctorName
	String
	✅
	Full name of the family doctor.
	contactInformation
	String
	✅
	Contact details of the family doctor
	city
	String
	✅
	City where the doctor is located.
	createdBy
	String
	✅
	ID of the user who created the entry.
	sateName
	String
	✅
	State or region where the doctor is located.
	countryName
	String
	✅
	Country where the doctor is located.   
	markAsImportant
	Boolean
	✅
	Indicates if the doctor's entry is marked as important.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	

	HTTP status code
	success
	Boolean
	

	true if the family doctor was created successfully.
	message
	String
	

	Human-readable message indicating the outcome of the operation.
	error
	String
	

	Error message if the request failed; null on success.
	id
	Int
	

	Newly created family doctor record ID
	userId
	String
	✅
	ID of the user who created the entry.
	typeId
	Int
	✅
	Unique identifier for the doctor type.
	typeaName
	String
	✅


	Name of the doctor type. If "Others" is selected, specify the custom doctor type.
	doctorName
	String
	✅
	Full name of the family doctor.
	contactInformation
	String
	✅
	Contact details of the family doctor
	city
	String
	✅
	City where the doctor is located.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedBy
	String
	✅


	ID of the user who last updated the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedAt
	String
	✅
	Timestamp of the last update.
	stateName
	String
	✅
	State or region where the doctor is located.
	countryName
	String
	✅
	Country where the doctor is located.   
	markAsImportant
	Boolean
	✅
	Indicates if the doctor's entry is marked as important.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	

API: CreateMedicationAllergy
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who created the entry.
	treatment_name
	Int
	✅
	The name or identifier of the treatment associated with the medication allergy.
	purpose
	String
	✅


	The reason or medical purpose for prescribing the medication.
	medicine_name
	String
	✅
	The name of the medication associated with the allergy.
	dosage
	String
	✅
	The dosage instructions for the medication.
	start_date
	String
	✅
	The date when the medication or treatment began.
	end_date
	String
	✅
	The date when the medication or treatment is scheduled to end.
	frequency_dosage
	String
	✅
	The frequency at which the medication is taken.
	side_effect
	String
	✅
	Any side effects or allergic reactions associated with the medication.
	files
	[noteFiles]
	✅
	A list of files related to the medication or allergy.
	markAsImportant
	Boolean
	✅
	A flag indicating whether the entry should be marked as important.
	🔹 Nested Type: File
Field
	Type
	Required
	Description
	file
	Byte
	✅
	Unique identifier of the question.
	originalFilename
	String
	✅
	A string containing the text content of the question displayed in the form.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅


	true if the Medication/Allergy was created successfully.
	message
	String
	✅


	Human-readable message indicating the outcome of the operation.
	error
	String
	



	Error message if the request failed; null on success.
	medicationId
	Int
	✅


	Newly created Medication/Allergy record ID
	recordId
	String
	✅
	Unique UUID for traceability.
	

API: CreateNote
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who created the entry.
	note_content
	String
	✅
	The content or text of the note, describing relevant details.
	created_by
	String
	✅


	ID of the user who created the entry.
	files
	[noteFiles]
	✅
	A list of files related to the note.
	markAsImportant
	Boolean
	✅
	A flag indicating whether the note should be marked as important (true/false).
	🔹 Nested Type: File
Field
	Type
	Required
	Description
	file
	Byte
	✅
	Unique identifier of the question.
	originalFilename
	String
	✅
	A string containing the text content of the question displayed in the form.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅


	true if the note was created successfully.
	message
	String
	✅


	Human-readable message indicating the outcome of the operation.
	error
	String
	



	Error message if the request failed; null on success.
	id
	Int
	✅


	Newly created note record ID
	requestIdentifier
	String
	✅
	Unique UUID for traceability.
	

API: CreateHealthInsurance
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user who created the entry.
	memberName
	String
	✅
	The name of the member covered by the health insurance.
	memberId
	String
	✅


	The ID of the member covered by the health insurance.
	groupId
	String
	✅
	The group or policy under which the health insurance is registered.
	dependents
	[String]
	

	A list of names of dependents covered under the health insurance.
	files
	[File]
	

	List of file
	createdBy
	String
	

	ID of the user who created the entry.
	InsuranceTypeId
	Int
	

	The identifier for the type of health insurance
	othersValue
	String
	

	Additional details or custom information related to the health insurance entry.
	markAsImportant
	Boolean
	✅
	A flag indicating whether the health insurance entry should be marked as important (true/false).
	healthDependents
	[healthInsuranceDependents]
	

	A list of dependent details for individuals covered under the health insurance.
	🔹 Nested Type: File
Field
	Type
	Required
	Description
	file
	Byte
	✅
	Unique identifier of the question.
	originalFilename
	String
	✅
	A string containing the text content of the question displayed in the form.
	🔹 Nested Type: healthInsuranceDependents
Field
	Type
	Required
	Description
	fullName
	String
	✅
	The full name of the dependent covered under the health insurance.
	dob
	String
	✅
	The date of birth of the dependent.
	relationshipId
	Int
	

	The ID for the relationship of the dependent to the member.
	gender
	String
	

	The gender of the dependent.
	id
	Int
	

	The unique identifier for the dependent.
	

🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code
	success
	Boolean
	✅


	true if the note was created successfully.
	message
	String
	✅


	Human-readable message indicating the outcome of the operation.
	errorMessage
	String
	



	Error message if the request failed; null on success.
	id
	Int
	✅


	Newly created note record ID
	userId
	String
	✅
	ID of the user who created the entry.
	requestIdentifier
	String
	✅
	Unique UUID for traceability.
	memberName
	String
	✅
	The name of the member covered by the health insurance.
	memberId
	String
	✅


	The ID of the member covered by the health insurance.
	groupId
	String
	✅
	The group or policy under which the health insurance is registered.
	dependents
	[String]
	✅


	A list of names of dependents covered under the health insurance.
	files
	[File]
	

	List of file
	createdBy
	String
	✅
	ID of the user who created the entry.
	InsuranceTypeId
	Int
	✅
	The identifier for the type of health insurance
	othersValue
	String
	✅
	Additional details or custom information related to the health insurance entry.
	





API: getMainVaults
🔸 Request Payload
Field
	Type
	Required
	Description
	No input parameters required
	

	

	

	🔸 Response Fields
Field
	Type
	Required
	Description
	message
	String
	✅
	Status or informational message.
	success
	Boolean
	✅
	Indicates whether the request was successful.
	code
	Int
	✅
	HTTP-style status code (e.g. 200 for success).
	error
	String
	✅
	Error details, if any (empty string if none).
	vaults
	[Vaults]
	✅
	List of available vaults. Each entry includes ID and name.
	

🔹 Nested Type: Vaults
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the vault.
	name
	String
	✅
	Name of the vault.
	

API: getSubModules
🔸 Request Payload
Field
	Type
	Required
	Description
	mainVaultId
	Int
	✅
	ID of the main vault for which submodules are to be fetched.
	









🔸 Response Fields
Field
	Type
	Required
	Description
	message
	String
	✅
	Informational or status message.
	success
	Boolean
	✅
	Indicates if the request was successful.
	code
	Int
	✅
	HTTP-style response code (e.g., 200).
	error
	String
	✅
	Error message, if any (empty string if no error).
	modules
	[SubModules]
	✅
	List of submodules associated with the given main vault.
	🔹 Nested Type: SubModules
Field
	Type
	Required
	Description
	subModuleId
	Int
	✅
	Unique ID of the submodule.
	mainVaultId
	Int
	✅
	ID of the main vault this submodule belongs to.
	subModuleName
	String
	✅
	Name of the submodule.
	

User Service API Documentation
 
________________






API: CreateUser
Description:
Creates a new user with the provided details.
🔸 Request Payload (CreateUserRequest)
Field
	Type
	Required
	Description
	firstName
	String
	✅
	User's first name
	lastName
	String
	✅
	User's last name
	preferredName
	String
	 
	User's preferred name
	dob
	String
	✅
	Date of birth (format: yyyy-MM-dd)
	gender
	String
	✅
	User's gender
	primaryEmail
	String
	✅
	User's primary email address
	phoneNumber
	String
	 
	User's phone number
	createdBy
	String
	 
	Identifier of the creator
	profilePath
	String
	 
	Path to user's profile image
	password
	String
	✅
	User's password
	Nationality
	String
	 
	User's nationality
	countryId
	Int32
	 
	Country identifier
	idTypeId
	Int32
	 
	ID type identifier
	idNumber
	String
	 
	ID number
	🔸 Response Fields (User)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	writeKeys
	Bool
	 
	Indicates if write keys are set
	stage
	Int32
	 
	Current stage of user creation
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if creation was successful
	code
	Int32
	 
	Status code
	________________


API: TwoFAOTP
Description:
Generates and sends a Two-Factor Authentication OTP to the user.
🔸 Request Payload (TwoFAOTPRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	channel
	String
	✅
	Channel to send OTP (e.g., SMS, Email)
	purpose
	String
	 
	Purpose of OTP (e.g., login, reset)
	🔸 Response Fields (TwoFAOTPResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if OTP was sent
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: EmailOTP
Description:
Generates and sends an OTP to the user's email for verification.
🔸 Request Payload (EmailOTPRequest)
Field
	Type
	Required
	Description
	email
	String
	✅
	Email address to send OTP
	purpose
	String
	 
	Purpose of OTP (e.g., signup, reset)
	🔸 Response Fields (EmailOTPResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if OTP was sent
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: SetPhoneNumber
Description:
Sets or updates the user's phone number.
🔸 Request Payload (SetPhoneRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	phoneNumber
	String
	✅
	New phone number
	🔸 Response Fields (SetPhoneResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if phone number was set
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: Login
Description:
Authenticates a user and returns login details.
🔸 Request Payload (LoginRequest)
Field
	Type
	Required
	Description
	primaryEmail
	String
	✅
	User's primary email address
	password
	String
	✅
	User's password
	🔸 Response Fields (LoginResponse)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	token
	String
	✅
	Authentication token
	success
	Bool
	✅
	Indicates if login was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: UpdatePreferredName
Description:
Updates the user's preferred name and optionally their recovery email.
🔸 Request Payload (UpdatePreferredNameRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	preferredName
	String
	✅
	New preferred name
	recoveryEmail
	String
	 
	Recovery email address
	updatedBy
	String
	 
	Identifier of the updater
	🔸 Response Fields (UpdatePreferredNameResponse)
Field
	Type
	Required
	Description
	updatedBy
	String
	 
	Identifier of the updater
	errorMessage
	String
	 
	Error message if update fails
	________________


API: MobileNumberVerification
Description:
Verifies the user's mobile number using OTP.
🔸 Request Payload (VerifyNumberOtpRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	otp
	String
	✅
	OTP received by the user
	🔸 Response Fields (VerificationResponse)
Field
	Type
	Required
	Description
	verified
	Bool
	✅
	Indicates if OTP was verified
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________








API: SetPassword
Description:
Sets or updates the user's password.
🔸 Request Payload (SetPasswordRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	primaryEmail
	String
	✅
	User's primary email address
	password
	String
	✅
	New password
	confirmPassword
	String
	✅
	Confirmation of the new password
	🔸 Response Fields (SetPasswordResponse)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	passwordSet
	Bool
	✅
	Indicates if password was set
	errorMessage
	String
	 
	Error message if operation fails
	________________


API: VerifyEmailOTP
Description:
Verifies the OTP sent to the user's email.
🔸 Request Payload (VerifyEmailOTPRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	OTP
	String
	✅
	OTP received by the user
	🔸 Response Fields (VerifyEmailOTPResponse)
Field
	Type
	Required
	Description
	verified
	Bool
	✅
	Indicates if OTP was verified
	message
	String
	 
	Informational message
	________________


API: GetUserId
Description:
Fetches the user ID based on the provided email.
🔸 Request Payload (GetUserIdRequest)
Field
	Type
	Required
	Description
	email
	String
	✅
	Email address of the user
	🔸 Response Fields (GetUserIdResponse)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	________________


API: IdTypes
Description:
Fetches the list of available ID types.
🔸 Request Payload (google.protobuf.Empty)
No fields required.
🔸 Response Fields (IdTypeResponse)
Field
	Type
	Required
	Description
	idTypes
	IdType[]
	✅
	List of available ID types
	Nested Type: IdType
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the ID type
	name
	String
	✅
	Name of the ID type
	________________


API: GetUserRole
Description:
Fetches the role of the user.
🔸 Request Payload (GetUserRoleRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (GetUserRoleResponse)
Field
	Type
	Required
	Description
	role
	String
	✅
	Role of the user
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GenerateQRForProxy
Description:
Generates a QR code for inviting a Trusted Helper (proxy) and sends it via email/SMS.
🔸 Request Payload (GenerateQRForProxyRequest)
Field
	Type
	Required
	Description
	vaults
	topLevelvault[]
	 
	List of vaults to share with the proxy
	hours
	Int32
	 
	Number of hours the QR code is valid
	minutes
	Int32
	 
	Number of minutes the QR code is valid
	personalMessage
	String
	 
	Personal message to include in the invite
	isPresent
	Bool
	 
	Whether the trusted helper is physically present
	trustedHelperName
	String
	 
	Name of the trusted helper
	phoneNumber
	String
	 
	Phone number of the trusted helper
	emailId
	String
	 
	Email address of the trusted helper
	userId
	String
	✅
	User ID of the person sending the invite
	subModuleNames
	String[]
	 
	List of sub-module names to share
	Nested Type: topLevelvault
Field
	Type
	Required
	Description
	vaultId
	String
	✅
	Vault identifier
	vaultName
	String
	✅
	Name of the vault
	🔸 Response Fields (GenerateQRForProxyResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if QR generation and invite was successful
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if operation fails
	qrCodeImage
	String
	 
	Base64-encoded QR code image
	qrLink
	String
	 
	Link embedded in the QR code
	UserName
	String
	 
	Name of the user who sent the invite
	TrustedHelperUserId
	String
	 
	User ID of the trusted helper
	personaId
	String
	 
	Persona ID for the proxy
	sharedModuleIds
	Int32[]
	 
	List of shared module IDs
	________________


API: ProxyReLogin
Description:
Allows a proxy user to re-login using their credentials.
🔸 Request Payload (ProxyReLoginRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	passcode
	String
	✅
	Passcode for authentication
	🔸 Response Fields (ProxyLoginResponse)
Field
	Type
	Required
	Description
	token
	String
	✅
	Authentication token
	proxyId
	String
	✅
	Unique identifier for the proxy
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if login was successful
	code
	Int32
	 
	Status code
	________________


API: ProxyUserOptOut
Description:
Allows a proxy user to opt out and revoke their access.
🔸 Request Payload (ProxyUserOptOutRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	reason
	String
	 
	Reason for opting out
	🔸 Response Fields (ProxyUserOptOutResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if opt-out was successful
	code
	Int32
	 
	Status code
	________________


API: RevokeProxyAccess
Description:
Revokes access for a proxy user.
🔸 Request Payload (RevokeAccessRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	userId
	String
	✅
	User ID of the owner
	🔸 Response Fields (RevokeAccessResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if access was revoked
	code
	Int32
	 
	Status code
	________________


API: SignUpProxy
Description:
Registers a new proxy user (Trusted Helper) for a user.
🔸 Request Payload (SignUpProxyRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the owner
	trustedHelperName
	String
	✅
	Name of the trusted helper
	phoneNumber
	String
	 
	Phone number of the trusted helper
	emailId
	String
	✅
	Email address of the trusted helper
	passcode
	String
	✅
	Passcode for the trusted helper
	🔸 Response Fields (SignUpProxyResponse)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if signup was successful
	code
	Int32
	 
	Status code
	________________


API: VerifyPasscode
Description:
Verifies the passcode for a proxy user.
🔸 Request Payload (VerifyPasscodeRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	passcode
	String
	✅
	Passcode to verify
	🔸 Response Fields (VerifyPasscodeResponse)
Field
	Type
	Required
	Description
	verified
	Bool
	✅
	Indicates if passcode was correct
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: ProxyLogin
Description:
Allows a proxy user to log in using their credentials.
🔸 Request Payload (ProxyLoginRequest)
Field
	Type
	Required
	Description
	emailId
	String
	✅
	Email address of the proxy
	passcode
	String
	✅
	Passcode for authentication
	🔸 Response Fields (ProxyLoginResponse)
Field
	Type
	Required
	Description
	token
	String
	✅
	Authentication token
	proxyId
	String
	✅
	Unique identifier for the proxy
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if login was successful
	code
	Int32
	 
	Status code
	________________


API: GetMainVaults
Description:
Fetches the main vaults accessible to a user or proxy.
🔸 Request Payload (GetMainVaultsRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or proxy ID
	🔸 Response Fields (GetMainVaultsResponse)
Field
	Type
	Required
	Description
	vaults
	Vault[]
	✅
	List of main vaults
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if fetch was successful
	code
	Int32
	 
	Status code
	Nested Type: Vault
Field
	Type
	Required
	Description
	vaultId
	String
	✅
	Vault identifier
	vaultName
	String
	✅
	Name of the vault
	________________


API: GetSubModules
Description:
Fetches sub-modules for a given vault or user.
🔸 Request Payload (GetSubModulesRequest)
Field
	Type
	Required
	Description
	vaultId
	String
	✅
	Unique identifier for the vault
	userId
	String
	✅
	User ID or proxy ID
	🔸 Response Fields (GetSubModulesResponse)
Field
	Type
	Required
	Description
	subModules
	SubModule[]
	✅
	List of sub-modules
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if fetch was successful
	code
	Int32
	 
	Status code
	Nested Type: SubModule
Field
	Type
	Required
	Description
	subModuleId
	String
	✅
	Sub-module identifier
	name
	String
	✅
	Name of the sub-module
	________________


API: GetProxyUserMessage
Description:
Fetches a message or notification for a proxy user.
🔸 Request Payload (GetProxyUserMessageRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	🔸 Response Fields (GetProxyUserMessageResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Message or notification
	success
	Bool
	✅
	Indicates if fetch was successful
	code
	Int32
	 
	Status code
	________________


API: GetNationality
Description:
Fetches the list of available nationalities.
🔸 Request Payload (GetNationalityRequest)
Field
	Type
	Required
	Description
	 
	 
	 
	No fields required
	🔸 Response Fields (GetNationalityResponse)
Field
	Type
	Required
	Description
	nationalities
	Nationality[]
	✅
	List of available nationalities
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if fetch was successful
	code
	Int32
	 
	Status code
	Nested Type: Nationality
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the nationality
	name
	String
	✅
	Name of the nationality
	________________


API: ContactUs
Description:
Submits a contact or support request.
🔸 Request Payload (contactUsRequest)
Field
	Type
	Required
	Description
	name
	String
	✅
	Name of the person contacting
	email
	String
	✅
	Email address
	message
	String
	✅
	Message or inquiry
	🔸 Response Fields (contactUsResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if request was submitted
	code
	Int32
	 
	Status code
	________________


API: ThanksForRegisteringQR
Description:
Generates a "Thank You for Registering" QR code for the user.
🔸 Request Payload (ThanksForRegisteringQRRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (ThanksForRegisteringQRResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if QR was generated
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if operation fails
	qrCodeImage
	String
	 
	Base64-encoded QR code image
	qrLink
	String
	 
	Link embedded in the QR code
	________________


API: SignUpSubscriber
Description:
Registers a new subscriber user for a main user, capturing identity and contact details.
🔸 Request Payload (SubscriberSignupRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	userId
	String
	✅
	User ID of the main user
	firstName
	String
	✅
	Subscriber's first name
	lastName
	String
	✅
	Subscriber's last name
	middleName
	String
	 
	Subscriber's middle name
	email
	String
	✅
	Subscriber's email address
	phoneNumber
	String
	✅
	Subscriber's phone number
	govtTypeId
	Int32
	✅
	Government ID type identifier
	idNumber
	String
	✅
	Government ID number
	termsAccepted
	String
	✅
	Timestamp or flag for terms acceptance
	🔸 Response Fields (SubscriberSignupResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if signup was successful
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if operation fails
	data
	SubscriberData
	 
	Details of the registered subscriber
	Nested Type: SubscriberData
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	userId
	String
	✅
	User ID of the main user
	subscriberUserId
	String
	 
	Internal user ID for the subscriber
	firstName
	String
	✅
	Subscriber's first name
	endDate
	String
	 
	End date of the subscription
	sharedModules
	Modules[]
	 
	List of modules shared with the subscriber
	Nested Type: Modules
Field
	Type
	Required
	Description
	moduleId
	String
	✅
	Module identifier
	moduleName
	String
	✅
	Name of the module
	________________


API: VerifySubscriberPasscode
Description:
Verifies the passcode for a subscriber user.
🔸 Request Payload (SubscriberVerifyPasscodeRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	passcode
	String
	✅
	Passcode to verify
	🔸 Response Fields (SubscriberVerifyPasscodeResponse)
Field
	Type
	Required
	Description
	verified
	Bool
	✅
	Indicates if passcode was correct
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: RevokeSubscriberAccess
Description:
Revokes access for a subscriber user.
🔸 Request Payload (RevokeSubscriberRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	userId
	String
	✅
	User ID of the main user
	🔸 Response Fields (RevokeSubcriberResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if access was revoked
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if operation fails
	________________


API: GetDID
Description:
Fetches the Decentralized Identifier (DID) for a user or subscriber.
🔸 Request Payload (GetDIDRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	🔸 Response Fields (GetDIDResponse)
Field
	Type
	Required
	Description
	did
	String
	✅
	Decentralized Identifier (DID)
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: SubscriberOptOut
Description:
Allows a subscriber user to opt out and revoke their access.
🔸 Request Payload (SubscriberOptOutRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	reason
	String
	 
	Reason for opting out
	🔸 Response Fields (SubcriberOptOutResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if opt-out was successful
	code
	Int32
	 
	Status code
	________________


API: GetAccessEventDropdown
Description:
Fetches the list of available access events for subscribers.
🔸 Request Payload (GetAccessEventDropdownRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the main user
	🔸 Response Fields (GetAccessEventDropdownResponse)
Field
	Type
	Required
	Description
	events
	AccessEvent[]
	✅
	List of available access events
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: AccessEvent
Field
	Type
	Required
	Description
	eventId
	Int32
	✅
	Event identifier
	eventName
	String
	✅
	Name of the event
	________________


API: GetSubscriberAccessTypes
Description:
Fetches the list of available access types for subscribers.
🔸 Request Payload (GetSubscriberAccessTypesRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the main user
	🔸 Response Fields (GetSubscriberAccessTypesResponse)
Field
	Type
	Required
	Description
	accessTypes
	AccessType[]
	✅
	List of available access types
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: AccessType
Field
	Type
	Required
	Description
	accessTypeId
	Int32
	✅
	Access type identifier
	accessTypeName
	String
	✅
	Name of the access type
	________________


API: AssignSubscriber
Description:
Assigns a subscriber to a user and shares selected vaults/modules.
🔸 Request Payload (AssignSubscriberRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the main user
	emailId
	String
	✅
	Email address of the subscriber
	vaults
	Vault[]
	✅
	List of vaults to share
	aceessId
	Int32
	✅
	Access type identifier
	accessEventId
	Int32
	✅
	Access event identifier
	startDate
	String
	 
	Start date for access
	endDate
	String
	 
	End date for access
	personalMessage
	String
	 
	Personal message to subscriber
	relationship
	String
	 
	Relationship with the subscriber
	contactId
	String
	 
	Contact ID
	Nested Type: Vault
Field
	Type
	Required
	Description
	vaultId
	String
	✅
	Vault identifier
	vaultName
	String
	✅
	Name of the vault
	🔸 Response Fields (AssignSubscriberResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if assignment was successful
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if operation fails
	________________


API: SubscriberLogin
Description:
Authenticates a subscriber user and returns login details.
🔸 Request Payload (subscriberLoginRequest)
Field
	Type
	Required
	Description
	email
	String
	✅
	Subscriber's email address
	passcode
	String
	✅
	Passcode for authentication
	🔸 Response Fields (subscriberLoginResponse)
Field
	Type
	Required
	Description
	token
	String
	✅
	Authentication token
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if login was successful
	code
	Int32
	 
	Status code
	________________


API: GetUserDetails
Description:
Fetches detailed information about a subscriber user.
🔸 Request Payload (GetUserDetailsRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (GetUserDetailsResponse)
Field
	Type
	Required
	Description
	details
	UserDetails
	✅
	Detailed information about the subscriber
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: UserDetails
Field
	Type
	Required
	Description
	name
	String
	✅
	Name of the subscriber
	email
	String
	✅
	Email address
	phone
	String
	 
	Phone number
	________________


API: CheckAssigne
Description:
Checks if a subscriber is assigned to a user.
🔸 Request Payload (CheckAssigneRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the main user
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (CheckAssigneResponse)
Field
	Type
	Required
	Description
	assigned
	Bool
	✅
	Indicates if subscriber is assigned
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: TransferOwnership
Description:
Transfers ownership of a record or vault to another user.
🔸 Request Payload (TransferOwnershipRequest)
Field
	Type
	Required
	Description
	fromUserId
	String
	✅
	Current owner user ID
	toUserId
	String
	✅
	New owner user ID
	recordId
	String
	✅
	Record or vault identifier
	🔸 Response Fields (TransferOwnershipResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if transfer was successful
	code
	Int32
	 
	Status code
	________________


API: GetB4igoProfile
Description:
Fetches the B4igo profile for a user or subscriber.
🔸 Request Payload (GetProfileRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	🔸 Response Fields (GetProfileResponse)
Field
	Type
	Required
	Description
	profile
	Profile
	✅
	Profile details
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: Profile
Field
	Type
	Required
	Description
	name
	String
	✅
	Name of the user
	email
	String
	✅
	Email address
	phone
	String
	 
	Phone number
	________________


API: UpdateB4igoProfile
Description:
Updates the B4igo profile for a user or subscriber.
🔸 Request Payload (UpdateB4igoProfileRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	profile
	Profile
	✅
	Updated profile details
	Nested Type: Profile
Field
	Type
	Required
	Description
	name
	String
	✅
	Name of the user
	email
	String
	✅
	Email address
	phone
	String
	 
	Phone number
	🔸 Response Fields (UpdateB4igoProfileResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if update was successful
	code
	Int32
	 
	Status code
	________________


API: SetProfilePicture
Description:
Sets or updates the profile picture for a user or subscriber.
🔸 Request Payload (SetProfilePicRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	image
	Bytes
	✅
	Profile picture image data
	🔸 Response Fields (CommonMutaionAPIResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if operation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: DeleteProfilePicture
Description:
Deletes the profile picture for a user or subscriber.
🔸 Request Payload (DeleteProfilePicRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	🔸 Response Fields (CommonMutaionAPIResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if operation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetProfilePicture
Description:
Fetches the profile picture for a user or subscriber.
🔸 Request Payload (GetProfilePicRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	🔸 Response Fields (GetProfilePicResponse)
Field
	Type
	Required
	Description
	image
	Bytes
	✅
	Profile picture image data
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetSharedInfo
Description:
Fetches shared information for a user or subscriber.
🔸 Request Payload (GetSharedInfoRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	🔸 Response Fields (GetSharedInfoResponse)
Field
	Type
	Required
	Description
	sharedInfo
	SharedInfo
	✅
	Shared information details
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: SharedInfo
Field
	Type
	Required
	Description
	infoId
	String
	✅
	Shared info identifier
	details
	String
	 
	Details of the shared info
	________________


API: RemoveModuleAccess
Description:
Removes access to a module for a user or subscriber.
🔸 Request Payload (RemoveAccess)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	moduleId
	String
	✅
	Module identifier
	🔸 Response Fields (CommonMutaionAPIResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if operation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: RejectModuleAccess
Description:
Rejects access to a module for a user or subscriber.
🔸 Request Payload (RemoveAccess)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	moduleId
	String
	✅
	Module identifier
	🔸 Response Fields (rejectMouduleAccessResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if operation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: RejectSubModuleAccess
Description:
Rejects access to a sub-module for a user or subscriber.
🔸 Request Payload (RemoveAccess)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	moduleId
	String
	✅
	Module identifier
	🔸 Response Fields (rejectMouduleAccessResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if operation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetUnsharedVaults
Description:
Fetches the list of vaults not yet shared with a subscriber.
🔸 Request Payload (GetUnsharedVaultsReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the main user
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (GetUnsharedVaultsRes)
Field
	Type
	Required
	Description
	vaults
	Vault[]
	✅
	List of unshared vaults
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: Vault
Field
	Type
	Required
	Description
	vaultId
	String
	✅
	Vault identifier
	vaultName
	String
	✅
	Name of the vault
	________________


API: GetVisionDetailsList
Description:
Fetches the list of vision details for a user or subscriber.
🔸 Request Payload (GetVisionDetailsRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID or subscriber ID
	🔸 Response Fields (GetVisionDetailsResponse)
Field
	Type
	Required
	Description
	visionList
	VisionDetail[]
	✅
	List of vision details
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: VisionDetail
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the vision detail
	visionDetailType
	String
	✅
	Type of vision detail
	________________










API: refreshToken
Description:
Generates a new access token and refresh token for a user, given a valid refresh token.
🔸 Request Payload (RefreshAccessTokenRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	refreshToken
	String
	✅
	The refresh token previously issued
	🔸 Response Fields (RefreshAccessTokenResponse)
Field
	Type
	Required
	Description
	accessToken
	String
	✅
	Newly generated access token
	refreshToken
	String
	✅
	Newly generated refresh token
	success
	Bool
	✅
	Indicates if token refresh was successful
	code
	Int32
	 
	Status code
	errorMessage
	String
	 
	Error message if operation fails
	________________


API: confirmInitiateVoting
Description:
Confirms the initiation of a voting process for a user or subscriber.
🔸 Request Payload (ConfirmInitiateVotingRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	votingId
	String
	✅
	Unique identifier for the voting event
	🔸 Response Fields (ConfirmInitiateVotingResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if confirmation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: actionForVoting
Description:
Performs an action (approve/reject) for a voting event.
🔸 Request Payload (ActionForVotingRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	votingId
	String
	✅
	Unique identifier for the voting event
	action
	String
	✅
	Action to perform (e.g., "approve", "reject")
	🔸 Response Fields (ConfirmInitiateVotingResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if action was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetSubscriberVoting
Description:
Fetches voting details for a subscriber.
🔸 Request Payload (votingSubscriberRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (VotingSubscriberResponse)
Field
	Type
	Required
	Description
	votingDetails
	VotingDetail[]
	✅
	List of voting details for the subscriber
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: VotingDetail
Field
	Type
	Required
	Description
	votingId
	String
	✅
	Unique identifier for the voting event
	status
	String
	✅
	Status of the voting event
	createdAt
	String
	 
	Creation timestamp
	updatedAt
	String
	 
	Last update timestamp
	________________


API: HelloServer
Description:
Performs a server handshake for SIWE (Sign-In With Ethereum) authentication.
🔸 Request Payload (SiweHelloRequest)
Field
	Type
	Required
	Description
	nonce
	String
	✅
	Nonce for SIWE authentication
	🔸 Response Fields (SiweHelloResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: VerifySignature
Description:
Verifies a cryptographic signature for SIWE authentication.
🔸 Request Payload (VerifySignatureRequest)
Field
	Type
	Required
	Description
	message
	String
	✅
	The message that was signed
	signature
	String
	✅
	The cryptographic signature
	🔸 Response Fields (VerifySignatureResponse)
Field
	Type
	Required
	Description
	verified
	Bool
	✅
	Indicates if the signature is valid
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: StoreVC
Description:
Stores a Verifiable Credential (VC) for a user.
🔸 Request Payload (StoreVCRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	vcData
	String
	✅
	Verifiable Credential data (JSON)
	🔸 Response Fields (StoreVCResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if VC was stored successfully
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: StoreEncryptedBlob
Description:
Stores an encrypted data blob for a user.
🔸 Request Payload (StoreBlobRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	blob
	Bytes
	✅
	Encrypted data blob
	🔸 Response Fields (StoreBlobResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if blob was stored successfully
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: FetchEncryptedBlob
Description:
Fetches an encrypted data blob for a user.
🔸 Request Payload (FetchBlobRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	blobId
	String
	✅
	Identifier for the encrypted blob
	🔸 Response Fields (FetchBlobResponse)
Field
	Type
	Required
	Description
	blob
	Bytes
	✅
	Encrypted data blob
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetAuthIdForBackup
Description:
Fetches an authentication ID for backup purposes.
🔸 Request Payload (GetAuthIdForBackupRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (GetAuthIdForBackupResponse)
Field
	Type
	Required
	Description
	authId
	String
	✅
	Authentication ID for backup
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: SignupDIDVersion
Description:
Creates a new user with DID (Decentralized Identifier) support.
🔸 Request Payload (CreateUserWithDIDRequest)
Field
	Type
	Required
	Description
	firstName
	String
	✅
	User's first name
	lastName
	String
	✅
	User's last name
	dob
	String
	✅
	Date of birth
	gender
	String
	✅
	Gender
	primaryEmail
	String
	✅
	Primary email address
	didObjects
	didObject[]
	 
	List of DID objects
	Nationality
	String
	 
	Nationality
	countryId
	Int32
	 
	Country identifier
	idTypeId
	Int32
	 
	ID type identifier
	idNumber
	String
	 
	ID number
	terms_accepted
	Bool
	 
	Whether terms are accepted
	type
	Int32
	 
	Type of user
	userId
	String
	 
	User ID (for updates)
	Nested Type: didObject
Field
	Type
	Required
	Description
	didObjectDump
	String
	 
	DID object dump (serialized)
	isBackup
	Bool
	 
	Is this a backup DID
	isMedical
	Bool
	 
	Is this a medical DID
	🔸 Response Fields (User)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	writeKeys
	Bool
	 
	Indicates if write keys are set
	stage
	Int32
	 
	Current stage of user creation
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if creation was successful
	code
	Int32
	 
	Status code
	________________


API: SignUpSubscriberDIDVersion
Description:
Registers a new subscriber user with DID support.
🔸 Request Payload (SubscriberSignupDIDVersionRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	userId
	String
	✅
	User ID of the main user
	firstName
	String
	✅
	Subscriber's first name
	lastName
	String
	✅
	Subscriber's last name
	middleName
	String
	 
	Subscriber's middle name
	email
	String
	✅
	Subscriber's email address
	phoneNumber
	String
	✅
	Subscriber's phone number
	govtTypeId
	Int32
	✅
	Government ID type identifier
	idNumber
	String
	✅
	Government ID number
	termsAccepted
	String
	✅
	Timestamp or flag for terms acceptance
	didObjects
	didObject[]
	 
	List of DID objects
	dob
	String
	 
	Date of birth
	gender
	String
	 
	Gender
	Nested Type: didObject
Field
	Type
	Required
	Description
	didObjectDump
	String
	 
	DID object dump (serialized)
	isBackup
	Bool
	 
	Is this a backup DID
	isMedical
	Bool
	 
	Is this a medical DID
	🔸 Response Fields (SubscriberSignupResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if signup was successful
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if operation fails
	data
	SubscriberData
	 
	Details of the registered subscriber
	Nested Type: SubscriberData
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	userId
	String
	✅
	User ID of the main user
	subscriberUserId
	String
	 
	Internal user ID for the subscriber
	firstName
	String
	✅
	Subscriber's first name
	endDate
	String
	 
	End date of the subscription
	sharedModules
	Modules[]
	 
	List of modules shared with the subscriber
	Nested Type: Modules
Field
	Type
	Required
	Description
	moduleId
	String
	✅
	Module identifier
	moduleName
	String
	✅
	Name of the module
	________________


API: GetVC
Description:
Fetches a Verifiable Credential (VC) for a user.
🔸 Request Payload (GetVCRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	vcId
	String
	✅
	Identifier for the VC
	🔸 Response Fields (GetVCResponse)
Field
	Type
	Required
	Description
	vcData
	String
	✅
	Verifiable Credential data (JSON)
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetSubscriberDIDS
Description:
Fetches all DIDs (Decentralized Identifiers) for a subscriber.
🔸 Request Payload (GetSubscriberDIDSRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (GetSubscriberDIDSResponse)
Field
	Type
	Required
	Description
	dids
	didObject[]
	✅
	List of DID objects for the subscriber
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: didObject
Field
	Type
	Required
	Description
	didObjectDump
	String
	 
	DID object dump (serialized)
	isBackup
	Bool
	 
	Is this a backup DID
	isMedical
	Bool
	 
	Is this a medical DID
	________________


API: RevokeVC
Description:
Revokes a Verifiable Credential (VC) for a user.
🔸 Request Payload (RevokeVCRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	vcId
	String
	✅
	Identifier for the VC
	🔸 Response Fields (RevokeVCResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if VC was revoked successfully
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetB4igoDid
Description:
Fetches the B4igo Decentralized Identifier (DID) for a user.
🔸 Request Payload (GetDIDRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (GetDIDResponse)
Field
	Type
	Required
	Description
	did
	String
	✅
	Decentralized Identifier (DID)
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetPendingIssueDIDs
Description:
Fetches the list of pending DIDs for all subscribers of a user.
🔸 Request Payload (GetPendingIsuueRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (GetPendingIsuueResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if fetch was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	pendingSubs
	PendingSubscriber[]
	✅
	List of pending subscribers and their DIDs
	Nested Type: PendingSubscriber
Field
	Type
	Required
	Description
	name
	String
	✅
	Full name of the subscriber
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	sharedModules
	String
	 
	Shared modules with the subscriber
	dids
	PendingDID[]
	 
	List of DIDs for the subscriber
	email
	String
	 
	Email address of the subscriber
	contactNumber
	String
	 
	Contact number of the subscriber
	Nested Type: PendingDID
Field
	Type
	Required
	Description
	did
	String
	✅
	Decentralized Identifier (DID)
	is_backup
	Bool
	 
	Indicates if this DID is a backup
	________________


API: getByIDMyEmergencyBracelet
Description:
Retrieves emergency bracelet access details by user ID and bracelet ID.
🔸 Request Payload (getByIDMyEmergencyBraceletReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	id
	Int32
	✅
	Bracelet record ID
	pageType
	Int32
	✅
	Page type (1 or 2)
	🔸 Response Fields (getByIDMyEmergencyBraceletResp)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if fetch was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	dataemergencyByID
	dataemergencyByID
	 
	Emergency bracelet details
	Nested Type: dataemergencyByID
Field
	Type
	Required
	Description
	date
	String
	 
	Date of the bracelet record
	device
	String
	 
	Device type (e.g., "Bracelet")
	userId
	String
	 
	User ID associated with the bracelet
	userName
	String
	 
	User name or access type
	pageType
	Int32
	 
	Page type
	accessType
	String
	 
	Access type
	________________






API: UpdateBraceletMyEmergency
Description:
Updates emergency bracelet access details for a user.
🔸 Request Payload (updateMyEmerBraceleteReq)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Bracelet record ID
	userid
	String
	✅
	Unique identifier for the user
	notifySubscriber
	Bool
	 
	Whether to notify the subscriber
	notificationMessage
	String
	 
	Notification message to send
	revokeType
	String
	 
	Type of revocation ("hard" or "access")
	🔸 Response Fields (updateMyEmerBraceleteResp)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if update was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: SubmitConsentConfirmation
Description:
Submits a consent confirmation for a user or subscriber.
🔸 Request Payload (ConsentConfrimationRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	consentType
	String
	✅
	Type of consent being confirmed
	timestamp
	String
	 
	Timestamp of the confirmation
	🔸 Response Fields (ConsentConfrimationResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if confirmation was successful
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: setPasswordPdf
Description:
Sets or updates the password for a PDF document associated with a user.
🔸 Request Payload (setPasswordPdfReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	pdfId
	String
	✅
	Identifier for the PDF document
	password
	String
	✅
	New password for the PDF
	🔸 Response Fields (setPasswordPdfRes)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if operation fails
	success
	Bool
	✅
	Indicates if password was set
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: getVCbySubjectDID
Description:
Fetches a Verifiable Credential (VC) by subject DID.
🔸 Request Payload (getVCbySubjectDIDRequest)
Field
	Type
	Required
	Description
	subjectDID
	String
	✅
	Subject's Decentralized Identifier (DID)
	vcType
	String
	 
	Type of Verifiable Credential
	🔸 Response Fields (GetVCResponse)
Field
	Type
	Required
	Description
	vcData
	String
	✅
	Verifiable Credential data (JSON)
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: SignUpCustodian
Description:
Registers a new custodian for a user.
🔸 Request Payload (SignUpCustodianRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID of the main user
	custodianName
	String
	✅
	Name of the custodian
	email
	String
	✅
	Email address of the custodian
	phoneNumber
	String
	 
	Phone number of the custodian
	🔸 Response Fields (SignUpCustodianResponse)
Field
	Type
	Required
	Description
	custodianId
	String
	✅
	Unique identifier for the custodian
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if signup was successful
	code
	Int32
	 
	Status code
	________________


API: GetTrustedHelperDetailsEndPoint
Description:
Fetches details of a trusted helper (subscriber) for a user.
🔸 Request Payload (GetSubscriberRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (GetSubscriberResponse)
Field
	Type
	Required
	Description
	subscriber
	SubscriberInfo
	✅
	Details of the subscriber
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: SubscriberInfo
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	firstName
	String
	✅
	First name of the subscriber
	lastName
	String
	✅
	Last name of the subscriber
	email
	String
	✅
	Email address of the subscriber
	phoneNumber
	String
	 
	Phone number of the subscriber
	________________


API: IsExistingUser
Description:
Checks if a user already exists in the system.
🔸 Request Payload (existingUserRequest)
Field
	Type
	Required
	Description
	email
	String
	✅
	Email address to check
	🔸 Response Fields (existingUserRepsponse)
Field
	Type
	Required
	Description
	exists
	Bool
	✅
	Indicates if the user exists
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	

API: GetUserInfoByEmail
Description:
Fetches user information based on email address.
🔸 Request Payload (GetUserInfoByEmailRequest)
Field
	Type
	Required
	Description
	email
	String
	✅
	Email address of the user
	🔸 Response Fields (GetUserInfoByEmailResponse)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	firstName
	String
	 
	First name of the user
	lastName
	String
	 
	Last name of the user
	email
	String
	 
	Email address of the user
	phoneNumber
	String
	 
	Phone number of the user
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetCustodian
Description:
Fetches details of a custodian for a user.
🔸 Request Payload (GetCustodianRequest)
Field
	Type
	Required
	Description
	custodianId
	String
	✅
	Unique identifier for the custodian
	🔸 Response Fields (GetCustodianResponse)
Field
	Type
	Required
	Description
	custodian
	CustodianInfo
	✅
	Details of the custodian
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: CustodianInfo
Field
	Type
	Required
	Description
	custodianId
	String
	✅
	Unique identifier for the custodian
	name
	String
	✅
	Name of the custodian
	email
	String
	✅
	Email address of the custodian
	phoneNumber
	String
	 
	Phone number of the custodian
	________________


API: IsUserPresent
Description:
Checks if a user is present in the system by witness request.
🔸 Request Payload (SignUpAgentWitnessRequest)
Field
	Type
	Required
	Description
	witnessId
	String
	✅
	Unique identifier for the witness
	🔸 Response Fields (SignUpAgentWitnessResponse)
Field
	Type
	Required
	Description
	present
	Bool
	✅
	Indicates if the user is present
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetUserNameById
Description:
Fetches the user name by user ID.
🔸 Request Payload (GetUserNameByIdReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (GetUserNameByIdRes)
Field
	Type
	Required
	Description
	userName
	String
	✅
	Name of the user
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: VerifyCustodianPasscode
Description:
Verifies the passcode for a custodian.
🔸 Request Payload (VerifyPasscodeRequest)
Field
	Type
	Required
	Description
	custodianId
	String
	✅
	Unique identifier for the custodian
	passcode
	String
	✅
	Passcode to verify
	🔸 Response Fields (VerifyPasscodeResponse)
Field
	Type
	Required
	Description
	verified
	Bool
	✅
	Indicates if passcode was correct
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: ResendOtp
Description:
Resends an OTP to the user.
🔸 Request Payload (resendOtpRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	channel
	String
	 
	Channel to send OTP (e.g., SMS, Email)
	🔸 Response Fields (resendOtpResponse)
Field
	Type
	Required
	Description
	success
	Bool
	✅
	Indicates if OTP was resent
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetFilters
Description:
Fetches available filters for user data.
🔸 Request Payload (filtersRequest)
Field
	Type
	Required
	Description
	filterType
	String
	✅
	Type of filter to fetch
	🔸 Response Fields (filtersResponse)
Field
	Type
	Required
	Description
	filters
	String[]
	✅
	List of available filters
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: GetSharedModulesForPersona
Description:
Fetches shared modules for a specific persona.
🔸 Request Payload (SharedModulePersonaRequest)
Field
	Type
	Required
	Description
	personaId
	String
	✅
	Unique identifier for the persona
	🔸 Response Fields (SharedModulePersonaResponse)
Field
	Type
	Required
	Description
	modules
	Module[]
	✅
	List of shared modules
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	Nested Type: Module
Field
	Type
	Required
	Description
	moduleId
	String
	✅
	Module identifier
	moduleName
	String
	✅
	Name of the module
	________________


API: DaoBoolean
Description:
Performs a DAO boolean operation for a user.
🔸 Request Payload (DaoBooleanRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	operation
	String
	✅
	Operation to perform
	🔸 Response Fields (DaoBooleanResponse)
Field
	Type
	Required
	Description
	result
	Bool
	✅
	Result of the operation
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: UserSubscriptionInvoice
Description:
Fetches the subscription invoice for a user.
🔸 Request Payload (UserSubscriptionInvoiceRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier for the user
	🔸 Response Fields (UserSubscriptionInvoiceResponse)
Field
	Type
	Required
	Description
	invoice
	String
	✅
	Subscription invoice details
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: RevokeProxyAccessNew
Description:
Revokes proxy access for a user.
🔸 Request Payload (RevokeProxyRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	userId
	String
	✅
	User ID of the owner
	🔸 Response Fields (RevokeProxyResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if access was revoked
	code
	Int32
	 
	Status code
	________________


API: RevokeCustodian
Description:
Revokes a custodian for a user.
🔸 Request Payload (RevokeCustodianRequest)
Field
	Type
	Required
	Description
	custodianId
	String
	✅
	Unique identifier for the custodian
	userId
	String
	✅
	User ID of the owner
	🔸 Response Fields (RevokeCustodianResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if revocation was successful
	code
	Int32
	 
	Status code
	________________


API: EditProxyNew
Description:
Edits proxy details for a user.
🔸 Request Payload (EditProxyRequest)
Field
	Type
	Required
	Description
	proxyId
	String
	✅
	Unique identifier for the proxy
	userId
	String
	✅
	User ID of the owner
	newDetails
	String
	 
	New details for the proxy
	🔸 Response Fields (EditSubscriberResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if edit was successful
	code
	Int32
	 
	Status code
	________________


API: EditCustodianNew
Description:
Edits custodian details for a user.
🔸 Request Payload (EditCustodianRequest)
Field
	Type
	Required
	Description
	custodianId
	String
	✅
	Unique identifier for the custodian
	userId
	String
	✅
	User ID of the owner
	newDetails
	String
	 
	New details for the custodian
	🔸 Response Fields (EditSubscriberResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if edit was successful
	code
	Int32
	 
	Status code
	________________


API: CancelVaultAccess
Description:
Cancels vault access for a user.
🔸 Request Payload (CancelVaultAccessRequest)
Field
	Type
	Required
	Description
	vaultId
	String
	✅
	Unique identifier for the vault
	userId
	String
	✅
	User ID of the owner
	🔸 Response Fields (CancelVaultAccessResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if cancellation was successful
	code
	Int32
	 
	Status code
	________________


API: CheckSubscriber
Description:
Checks subscriber details for a user.
🔸 Request Payload (GetSubscriberCheckRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the subscriber
	🔸 Response Fields (GetSubscriberCheckResponse)
Field
	Type
	Required
	Description
	exists
	Bool
	✅
	Indicates if the subscriber exists
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________


API: CheckTrustedHelp
Description:
Checks trusted helper details for a user.
🔸 Request Payload (GetSubscriberCheckRequest)
Field
	Type
	Required
	Description
	subscriberId
	String
	✅
	Unique identifier for the trusted helper
	🔸 Response Fields (GetSubscriberCheckResponse)
Field
	Type
	Required
	Description
	exists
	Bool
	✅
	Indicates if the trusted helper exists
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	________________




List of PersonalInfo Microservice
Query:
   * getRelationshipStatus: Fetches a paginated list of relationship status records for a user.
   * getRelationshipStatusById: Fetches a single relationship status record by its ID and user ID.
   * relationshipStatusDropDown: Fetches a dropdown list of available relationship statuses for a given user.
   * getIdentityProofById: Fetches a specific identity proof record for a user by its ID.
   * getAllIdentityProofs: Fetches all identity proof records for a given user.
   * getDependentTypes: Fetches the list of available dependent types (e.g., child, spouse, parent) for use in forms or profile management.
   * getDependentDetailsById: Fetches the details of a specific dependent for a user by dependent ID.
   * getAllDependentDetails: Fetches all dependent records for a given user.
   * getIdentityProofTypes: Fetches all dependent records for a given user
   * getAddressTypes: Fetches the list of available address types (e.g., Home, ffice) for use in address forms.
   * GetAddressDetailsById: Fetches detailed address information for a specific address record by its ID and userId.
   * GetAllAddressDetails: Fetches a paginated list of all address records for a user, including detailed information and associated files.
   * getEducationByUserId: Fetches a paginated list of all education records for a user, including detailed information and associated files.
   * getEducationById: Fetches a single education record for a user by its ID and userId, including all details and associated files.
   * getSkillSets: Fetches the list of available skill sets in the system.
   * getContactByUserId: Fetches a paginated list of contact details for a user, with filtering options.
   * getContactById: Fetches a single contact record for a user by its ID and userId, including all details.
   * getContactType: Fetches the list of available contact types in the system.
   * getRelationTypes: Fetches the list of available relation types in the system.
   * getSalaryRange: Fetches the list of available salary ranges.
   * getEmploymentType: Fetches the list of available employment types.
   * getTypefEmployment: Fetches the list of available types of employment.
   * getEmploymentById: Fetches a specific employment record by its ID and user ID.
   * getAllEmployment: Fetches a paginated list of all employment records for a user.
   * getDashboard: Fetches dashboard progress and completion status for a user's vault, including submodules and their completion metrics
   * getAddressDependentsByUserId: Fetches a list of address dependents for a user, optionally filtered by current relation status.
   * getAddressDependentsById: Fetches the dependents related to a specific address for a given user by their ID.
   * printPdf: Generates and returns PDF-related data for a user, including identity proofs and address details, based on provided module IDs and vault ID.
   * emergencyContactBreclate: Fetch the contact bracelet by user Id
   * getIndustries: Fetches the list of available industries.
   * getSubCategories: Fetches the list of subcategories for a given industry.
   * getCertificationStatuses: Fetches the list of available certification statuses.
   * getProficiencyLevels: Fetches the list of available certification statuses.


Mutation:
   *  createRelationshipStatus: Creates a new relationship status record for a user.
   * updateRelationshipStatus: Updates an existing relationship status record for a user
   * deleteRelationshipStatus: Deletes a relationship status record for a user.
   * addIdentityProof: Add a new identity proof record for a user
   * updateIdentityProof: Updates an existing identity proof record for a user, including document details and file uploads.
   * deleteIdentityProof: Deletes an identity proof record for a user.
   * addDependent: Adds a new dependent record for a user.
   * deleteDependent: Deletes a dependent record for a user.
   * updateDependent: Updates an existing dependent record for a user.
   * addAddressDetails: Adds a new address record for a user, including address details and optional file uploads.
   * updateAddressDetails :Updates an existing address record for a user, including address details and optional file uploads.
   * deleteAddressDetails: Deletes an address record for a user by its unique ID.
   * createEducation: Creates a new education record for a user.
   * updateEducation: Updates an existing education record for a user.
   * deleteEducationById: Deletes an education record for a user by its unique ID.
   * createContact: Creates a new contact record for a user.
   * updateContact: Updates an existing contact record for a user.
   * deleteContact: Delete one or more contact records for a user by their IDs.
   * addEmployment: Add a new employment record for a user, including company, designation, employment type, salary range, address, tes, and supporting files.
   * updateEmployment: Update an existing employment record for a user, including company, designation, employment type, salary range, address, tes, and supporting files.
   * deleteEmployment: Delete an employment record for a user by its ID.
   * addRelationAndDependents: Add one or more relation and dependent records for a user, including address, relation/dependent details, files, and metadata.
   * updateRelationAndDependents: Update one or more relation and dependent records for a user, including address, relation/dependent details, files, and metadata.
   * deleteFilesRD: Delete a file associated with a relation or dependent record for a user.
   * deleteRelationDependents: Delete a relation or dependent record by its ID.
   * deleteRelationDependentsById: Deletes a specific relation or dependent record by its ID, user ID, and type.
   * fileReUpload: mutation is to allow a user to re-upload or replace an existing file associated with a record
   * addSkillSets: mutation is to allow users to add multiple skill sets, organized by industry and category, to their profile. It enables bulk creation of skills, including details like proficiency, certification, experience, and associated files, helping users comprehensively manage and update their professional skill information.
   * deleteSkillSet: mutation is to allow a user to remove a specific skill from their profile, identified by user, industry, category, and skill IDs. This helps users manage and update their skill records by deleting outdated or incorrect skill entries.
API List
 API: getRelationshipStatus
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	User's unique identifier
	count
	Int
	✅
	Number of records per page
	page
	Int
	✅
	Page number
	🔸 Response Fields


Field
	Type
	Required
	Description
	records
	[RelationshipStatus]!
	✅
	List of relationship status records
	errorMessage
	String!
	✅
	Error message, if any
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Informational message
	code
	Int!
	✅
	Status code
	

🔹 Nested Type: RelationshipStatus


Field
	Type
	Required
	Description
	relationshipTypeId
	Int!
	✅
	Relationship type ID
	relationshipStatus
	String!
	✅
	Status of the relationship
	isCurrentRelationship
	Boolean!
	✅
	Is this the current relationship?
	startDate
	String!
	✅
	Start date
	endDate
	String
	

	End date
	tes
	String
	

	tes
	createdBy
	String!
	✅
	Created by
	updatedBy
	String!
	✅
	Updated by
	createdAt
	String!
	✅
	Created at
	updatedAt
	String!
	✅
	Updated at
	files
	[RelationshipStatusFile!]!
	✅
	List of related files
	id
	Int!
	✅
	Record ID
	userId
	String!
	✅
	User's unique identifier
	

API: getRelationshipStatusById
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Relationship status ID
	userId
	String!
	✅
	User's unique identifier
	🔸 Response Fields


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Record ID
	relationshipTypeId
	Int!
	✅
	Relationship type ID
	relationshipStatus
	String!
	✅
	Status of the relationship
	isCurrentRelationship
	Boolean!
	✅
	Is this the current relationship?
	startDate
	String!
	✅
	Start date
	endDate
	String
	

	End date
	tes
	String
	

	tes
	createdBy
	String!
	✅
	Created by
	updatedBy
	String!
	✅
	Updated by
	createdAt
	String!
	✅
	Created at
	updatedAt
	String!
	✅
	Updated at
	files
	[RelationshipStatusFile]!
	✅
	List of related files
	errorMessage
	String!
	✅
	Error message, if any
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Informational message
	code
	Int!
	✅
	Status code
	userId
	String!
	✅
	User's unique identifier
	

🔹 Nested Type: RelationshipStatusFile


Field Name
	Type
	Required
	Description
	fileUrl
	String
	✅
	URL to access the file
	fileContent
	String
	✅
	Content of the file (likely base64 or text)
	originalFilename
	String
	✅
	riginal name of the uploaded file
	createdBy
	String
	✅
	User who created the file
	updatedBy
	String
	✅
	User who last updated the file
	createdAt
	String
	✅
	Timestamp when file was created
	updatedAt
	String
	✅
	Timestamp when file was updated
	id
	Int
	✅
	Unique identifier for the file
	



 API: relationshipStatusDropDown
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	The user's unique ID
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	options
	[RelationshipStatusUnit!]!
	✅
	List of available relationship statuses
	

🔹 Nested Type: RelationshipStatusUnit
Field Name
	Type
	Required
	Description
	relationshipStatus
	String
	✅
	Name of the relationship status
	id
	Int
	✅
	Unique identifier
	

 Api: getIdentityProofById
🔸 Request Payload


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	The unique ID of the identity proof
	userId
	String
	✅
	The user's unique ID
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	message
	String!
	✅
	Response message
	success
	Boolean!
	✅
	Indicates if the request was successful
	code
	Int!
	✅
	Status or error code
	error
	String!
	✅
	Error message if any
	data
	IdentityProof!
	✅
	The identity proof record
	

 API: getAllIdentityProofs
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	The user's unique ID
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	identityProofs
	[IdentityProof!]!
	✅
	List of all identity proofs for the user
	code
	Int!
	✅
	Status or error code
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Response message
	error
	String
	

	Error message if any
	

🔹 Nested Type: IdentityProof
Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique identifier
	userId
	String!
	✅
	User's unique ID
	identityProofTypeId
	Int!
	✅
	Type ID of the identity proof
	identityProofType
	String
	

	Name/type of the identity proof
	nationality
	String
	

	Nationality
	documentNumber
	String
	

	Document number
	createdBy
	String!
	✅
	Who created the record
	updatedBy
	String!
	✅
	Who last updated the record
	createdAt
	String!
	✅
	Creation timestamp
	updatedAt
	String!
	✅
	Last update timestamp
	files
	[IdentityProofFiles!]!
	✅
	List of attached files
	subTitle
	String
	

	Subtitle or extra info
	recordIdentifier
	String!
	✅
	Record identifier
	

 API: getDependentTypes
🔸 Request Payload
thing
🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int!
	✅
	Status or error code
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Response message
	dependents
	[Dependents!]!
	✅
	List of available dependent types
	error
	String
	

	Error message if any
	

🔹 Nested Type: Dependents
Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique identifier for the dependent type
	dependent
	String!
	✅
	Name of the dependent type
	

 API: getDependentDetailsById
🔸 Request Payload


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	The unique ID of the dependent
	userId
	String
	✅
	The user's unique ID
	

🔸 Response Fields


Field Name
	Type
	Required
	Description
	message
	String!
	✅
	Response message
	success
	Boolean!
	✅
	Indicates if the request was successful
	code
	Int!
	✅
	Status or error code
	error
	String!
	✅
	Error message if any
	dependentDetails
	Dependent!
	✅
	The dependent's details
	

🔹 Nested Type: Dependent
Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique identifier for the dependent
	userId
	String!
	✅
	User's unique ID
	dependentTypeId
	Int!
	✅
	Type ID of the dependent
	dependentType
	String!
	✅
	Name/type of the dependent
	dependentName
	String!
	✅
	Name of the dependent
	dob
	String!
	✅
	Date of birth
	tes
	String!
	✅
	tes about the dependent
	createdBy
	String!
	✅
	Who created the record
	updatedBy
	String!
	✅
	Who last updated the record
	createdAt
	String!
	✅
	Creation timestamp
	updatedAt
	String!
	✅
	Last update timestamp
	

 API: getAllDependentDetails
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	The user's unique ID
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	dependentDetails
	[Dependent!]!
	✅
	List of all dependents for the user
	code
	Int!
	✅
	Status or error code
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Response message
	error
	String
	

	Error message if any
	

🔹 Nested Type: Dependent
Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique identifier for the dependent
	userId
	String!
	✅
	User's unique ID
	dependentTypeId
	Int!
	✅
	Type ID of the dependent
	dependentType
	String!
	✅
	Name/type of the dependent
	dependentName
	String!
	✅
	Name of the dependent
	dob
	String!
	✅
	Date of birth
	tes
	String!
	✅
	tes about the dependent
	createdBy
	String!
	✅
	Who created the record
	updatedBy
	String!
	✅
	Who last updated the record
	createdAt
	String!
	✅
	Creation timestamp
	updatedAt
	String!
	✅
	Last update timestamp
	

 API: getIdentityProofTypes
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	The user's unique ID
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	dependentDetails
	[Dependent!]!
	✅
	List of all dependents for the user
	code
	Int!
	✅
	Status or error code
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Response message
	error
	String
	

	Error message if any
	

Nested-Type: Dependent


Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique identifier for the dependent
	userId
	String!
	✅
	User's unique ID
	dependentTypeId
	Int!
	✅
	Type ID of the dependent
	dependentType
	String!
	✅
	Name/type of the dependent
	dependentName
	String!
	✅
	Name of the dependent
	dob
	String!
	✅
	Date of birth
	tes
	String!
	✅
	tes about the dependent
	createdBy
	String!
	✅
	Who created the record
	updatedBy
	String!
	✅
	Who last updated the record
	createdAt
	String!
	✅
	Creation timestamp
	updatedAt
	String!
	✅
	Last update timestamp
	

 API: getAddressTypes
🔸 Request Payload
thing
🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int!
	✅
	Status or error code
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Response message
	addressTypes
	[AddressTypes!]!
	✅
	List of available address types
	error
	String
	

	Error message if any
	

Nested Types: AddressTypes


Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique identifier for the address type
	typefAddress
	String!
	✅
	Name of the address type
	

 API: GetAddressDetailsById
🔸 Request Payload


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	Address record ID
	userId
	String
	✅
	User identifier
	🔸 Response Fields


Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	peration success flag
	message
	String
	✅
	Response message
	addressDetailsById
	AddressDetailsById
	✅
	Detailed address info (see below)
	error
	String
	

	Error message if any
	

Nested Type: AddressDetailsById


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	Address ID
	userId
	String
	✅
	User identifier
	addressTypeId
	Int
	✅
	Address type ID
	typefAddress
	String
	✅
	Type of address
	companyName
	String
	

	Company name (if applicable)
	streetNameAndNumber
	String
	✅
	Street name and number
	apartmentUnitNumber
	String
	✅
	Apartment/unit number
	city
	String
	✅
	City
	state
	String
	✅
	State
	country
	String
	✅
	Country
	pincode
	String
	✅
	Postal code
	isCurrentAddress
	Boolean
	

	Is this the current address?
	startDate
	String
	✅
	Start date
	endDate
	String
	

	End date
	createdBy
	String
	

	Created by
	updatedBy
	String
	

	Updated by
	createdAt
	String
	

	Creation timestamp
	updatedAt
	String
	

	Update timestamp
	files
	[Addressfiles!]
	✅
	List of address files (see below)
	

Nested Type: Addressfiles


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	File ID
	addressId
	Int
	✅
	Associated address ID
	documentFileLink
	String
	✅
	File download link
	originalFileName
	String
	✅
	riginal file name
	createdBy
	String
	✅
	File created by
	updatedBy
	String
	✅
	File updated by
	createdAt
	String
	✅
	File creation timestamp
	updatedAt
	String
	✅
	File update timestamp
	

 API: GetAllAddressDetails
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	limit
	Int
	✅
	Number of records per page
	page
	Int
	✅
	Page number
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	message
	String
	✅
	Response message
	success
	Boolean
	✅
	peration success flag
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	addressDetails
	[AllAddressDetails]!
	✅
	List of address records (see below)
	totalPages
	Int
	✅
	Total number of pages
	totalRecords
	Int
	✅
	Total number of records
	currentPage
	Int
	✅
	Current page number
	

Nested Types: AllAddressDetails


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	Address ID
	userId
	String
	✅
	User identifier
	addressTypeId
	Int
	✅
	Address type ID
	typefAddress
	String
	✅
	Type of address
	streetNameAndNumber
	String
	✅
	Street name and number
	apartmentUnitNumber
	String
	✅
	Apartment/unit number
	city
	String
	✅
	City
	state
	String
	✅
	State
	country
	String
	✅
	Country
	pincode
	String
	✅
	Postal code
	isCurrentAddress
	Boolean
	

	Is this the current address?
	startDate
	String
	✅
	Start date
	endDate
	String
	

	End date
	createdBy
	String
	

	Created by
	updatedBy
	String
	

	Updated by
	createdAt
	String
	

	Creation timestamp
	updatedAt
	String
	

	Update timestamp
	files
	[Addressfiles!]
	✅
	List of address files (see below)
	subTitle
	String
	

	Subtitle (if any)
	recordIdentifier
	String
	✅
	Unique record identifier
	

Nested Types: Addressfiles


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	File ID
	addressId
	Int
	✅
	Associated address ID
	documentFileLink
	String
	✅
	File download link
	originalFileName
	String
	✅
	riginal file name
	createdBy
	String
	✅
	File created by
	updatedBy
	String
	✅
	File updated by
	createdAt
	String
	✅
	File creation timestamp
	updatedAt
	String
	✅
	File update timestamp
	

 API: getEducationByUserId
🔸 Request Payload


Parameter
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	page
	Int
	✅
	Page number
	count
	Int
	✅
	Number of records per page
	others
	String
	✅
	Additional filter or value
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	success
	Boolean
	✅
	peration success flag
	message
	String
	✅
	Response message
	code
	Int
	✅
	Status code
	totalRecords
	Int
	✅
	Total number of records
	currentPage
	Int
	✅
	Current page number
	totalPages
	Int
	✅
	Total number of pages
	records
	[EducationDetails]!
	✅
	List of education records (see below)
	

Nested Types: EducationDetails


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	File ID
	educationId
	Int
	✅
	Associated education ID
	documentFileLink
	String
	✅
	File download link
	originalFileName
	String
	✅
	riginal file name
	createdBy
	String
	✅
	File created by
	updatedBy
	String
	✅
	File updated by
	createdAt
	String
	✅
	File creation timestamp
	updatedAt
	String
	✅
	File update timestamp
	

 API: getEducationById
🔸 Request Payload


Parameter
	Type
	Required
	Description
	id
	Int
	✅
	Education record ID
	userId
	String
	✅
	User identifier
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	success
	Boolean
	✅
	peration success flag
	message
	String
	✅
	Response message
	code
	Int
	✅
	Status code
	record
	EducationDetails
	

	Education record details (see below)
	

Nested Type: EducationDetails


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	Education record ID
	educationCertificateId
	Int
	✅
	Certificate ID
	educationCertificateName
	String
	✅
	Certificate name
	nameAsPerCertificate
	String
	✅
	Name as per certificate
	universityrCollegeName
	String
	✅
	University or college name
	roll
	String
	

	Roll number
	completionYear
	Int
	

	Year of completion
	isCurrentlyPursuing
	Boolean
	✅
	Currently pursuing flag
	startDate
	String
	

	Start date
	endDate
	String
	

	End date
	userId
	String
	✅
	User identifier
	createdAt
	String
	

	Creation timestamp
	updatedAt
	String
	

	Update timestamp
	createdBy
	String
	

	Created by
	updatedBy
	String
	

	Updated by
	status
	Boolean
	

	Status flag
	files
	[EducationFiles]!
	✅
	List of education files (see below)
	subTitle
	String
	

	Subtitle (if any)
	recordIdentifier
	String
	✅
	Unique record identifier
	

Nested Type: EducationFiles


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	File ID
	educationId
	Int
	✅
	Associated education ID
	documentFileLink
	String
	✅
	File download link
	originalFileName
	String
	✅
	riginal file name
	createdBy
	String
	✅
	File created by
	updatedBy
	String
	✅
	File updated by
	createdAt
	String
	✅
	File creation timestamp
	updatedAt
	String
	✅
	File update timestamp
	

 API: getSkillSets
🔸 Request Payload
thing
🔸 Response Fields


Field Name
	Type
	Required
	Description
	skills
	[SkillSet]!
	✅
	List of skill sets (see below)
	message
	String
	

	Response message
	code
	Int
	

	Status code
	success
	Boolean
	

	peration success flag
	

Nested Type: SkillSet


Field Name
	Type
	Required
	Description
	id
	Int
	✅
	Skill/certificate ID
	certificateName
	String
	✅
	Name of the certificate
	

 API: getContactByUserId
🔸 Request Payload


Parameter
	Type
	Required
	Description
	request
	GetContactByUserIdRequest
	✅
	Input object with userId, page, count, and filters
	Nested Type: GetContactByUserIdRequest
Field Name
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	page
	Int
	✅
	Page number
	count
	Int
	✅
	Number of records per page
	filters
	Filters
	✅
	Filtering options
	Nested Type: Filters


Field Name
	Type
	Required
	Description
	search
	String
	✅
	Search string
	contactTypeIds
	[Int!]
	✅
	List of contact type IDs
	isSubscriber
	Boolean
	✅
	Filter by subscriber status
	isTrustedHelper
	Boolean
	✅
	Filter by trusted helper status
	isWitness
	Boolean
	✅
	Filter by witness status
	isCustodian
	Boolean
	✅
	Filter by custodian status
	isPowerfAttorney
	Boolean
	✅
	Filter by power of attorney status
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	success
	Boolean
	✅
	peration success flag
	message
	String
	✅
	Response message
	code
	Int
	✅
	Status code
	totalRecords
	Int
	✅
	Total number of records
	currentPage
	Int
	✅
	Current page number
	totalPages
	Int
	✅
	Total number of pages
	contactDetails
	[ContactDetails]!
	✅
	List of contact records (see below)
	

Nested Type: ContactDetails


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	contactTypeId
	[Int!]
	✅
	List of contact type IDs
	name
	String
	✅
	Contact name
	contactNumber
	String
	✅
	Contact number
	companyName
	String
	✅
	Company name
	employeeId
	String
	✅
	Employee ID
	relationship
	String
	✅
	Relationship
	emailId
	String
	✅
	Email address
	streetNameAndNumber
	String
	

	Street name and number
	apartmentNumber
	String
	

	Apartment number
	city
	String
	

	City
	state
	String
	

	State
	pincode
	String
	

	Postal code
	country
	String
	

	Country
	createdBy
	String
	

	Created by
	createdAt
	String
	

	Creation timestamp
	updatedBy
	String
	

	Updated by
	updatedAt
	String
	

	Update timestamp
	id
	Int
	✅
	Contact record ID
	relationId
	Int
	

	Relation ID
	others
	String
	

	ther info
	jobRole
	String
	

	Job role
	subTitle
	String
	

	Subtitle
	recordIdentifier
	String
	✅
	Unique record identifier
	dob
	String
	

	Date of birth
	isDeceased
	Boolean
	

	Is deceased
	datefDeath
	String
	

	Date of death
	

 API: getContactById
🔸 Request Payload


Parameter
	Type
	Required
	Description
	id
	Int
	✅
	Contact record ID
	userId
	String
	✅
	User identifier
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	success
	Boolean
	✅
	peration success flag
	message
	String
	✅
	Response message
	code
	Int
	✅
	Status code
	record
	ContactDetails
	✅
	Contact record details (see below)
	

Nested Type: ContactDetails


Field Name
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	contactTypeId
	[Int!]
	✅
	List of contact type IDs
	name
	String
	✅
	Contact name
	contactNumber
	String
	✅
	Contact number
	companyName
	String
	✅
	Company name
	employeeId
	String
	✅
	Employee ID
	relationship
	String
	✅
	Relationship
	emailId
	String
	✅
	Email address
	streetNameAndNumber
	String
	

	Street name and number
	apartmentNumber
	String
	

	Apartment number
	city
	String
	

	City
	state
	String
	

	State
	pincode
	String
	

	Postal code
	country
	String
	

	Country
	createdBy
	String
	

	Created by
	createdAt
	String
	

	Creation timestamp
	updatedBy
	String
	

	Updated by
	updatedAt
	String
	

	Update timestamp
	id
	Int
	✅
	Contact record ID
	relationId
	Int
	

	Relation ID
	others
	String
	

	ther info
	jobRole
	String
	

	Job role
	subTitle
	String
	

	Subtitle
	recordIdentifier
	String
	✅
	Unique record identifier
	dob
	String
	

	Date of birth
	isDeceased
	Boolean
	

	Is deceased
	datefDeath
	String
	

	Date of death
	

 API: getContactType
🔸 Request Payload
ne
🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	message
	String
	

	Response message
	success
	Boolean
	✅
	peration success flag
	contacts
	[ContactTypes]!
	✅
	List of contact types (see below)
	

Nested Type: ContactTypes


Field Name
	Type
	Required
	Description
	contactId
	Int
	✅
	Contact type ID
	contactName
	String
	✅
	Name of the contact type
	

 API: getRelationTypes
🔸 Request Payload
ne
🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	message
	String
	

	Response message
	success
	Boolean
	✅
	peration success flag
	relationTypes
	[RelationTypes]!
	✅
	List of relation types (see below)
	

Nested Type: RelationTypes


Field Name
	Type
	Required
	Description
	relationId
	Int
	✅
	Relation type ID
	relationName
	String
	✅
	Name of the relation type
	

 API: getSalaryRange
🔸 Request Payload
ne
🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code of the response
	success
	Boolean
	✅
	Indicates if the request was successful
	message
	String
	✅
	Response message
	salaryRange
	[SalaryRange!]!
	✅
	List of salary range objects
	error
	String
	

	Error message if any
	

Nested Types: SalaryRange
Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique ID
	salaryRange
	String!
	✅
	Salary range label
	

 API: getEmploymentType
🔸 Request Payload
ne
🔸 Response Fields


Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code of the response
	success
	Boolean
	✅
	Indicates if the request was successful
	message
	String
	✅
	Response message
	employmentType
	[EmploymentType!]!
	✅
	List of employment type objects
	error
	String
	

	Error message if any
	

Nested Type: EmploymentType


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Unique ID
	employmentType
	String!
	✅
	Employment type name
	

 API: getTypefEmployment
🔸 Request Payload
ne
🔸 Response Fields


Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code of the response
	success
	Boolean
	✅
	Indicates if the request was successful
	message
	String
	✅
	Response message
	typefEmployment
	[TypefEmployment!]!
	✅
	List of type of employment objects
	error
	String
	

	Error message if any
	

Nested Type: TypefEmployment


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Unique ID
	typefEmployment
	String!
	✅
	Type of employment name
	

 API: getEmploymentById
🔸 Request Payload


Parameter
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID
	userId
	String!
	✅
	User's unique identifier
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int!
	✅
	Status code of the response
	success
	Boolean!
	✅
	Indicates if the request was successful
	message
	String!
	✅
	Response message
	employment
	Employment!
	✅
	Employment record object
	error
	String
	

	Error message if any
	

Nested Type: Employment


Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID
	userId
	String!
	✅
	User's unique identifier
	employmentTypeId
	Int!
	✅
	Employment type ID
	employmentType
	String!
	✅
	Employment type name
	companyName
	String!
	✅
	Company name
	designation
	String!
	✅
	Designation
	salaryRangeId
	Int!
	✅
	Salary range ID
	salaryRange
	String!
	✅
	Salary range label
	typefEmploymentId
	Int!
	✅
	Type of employment ID
	typefEmployment
	String!
	✅
	Type of employment name
	streetNameAndNumber
	String!
	✅
	Street address
	apartmentUnitNumber
	String!
	✅
	Apartment/unit number
	city
	String!
	✅
	City
	state
	String!
	✅
	State
	country
	String!
	✅
	Country
	pincode
	String!
	✅
	Pincode
	currentEmployment
	Boolean!
	✅
	Is this the current employment
	startDate
	String!
	✅
	Start date
	endDate
	String!
	✅
	End date
	createdAt
	String!
	✅
	Created at
	updatedAt
	String!
	✅
	Updated at
	createdBy
	String!
	✅
	Created by
	updatedBy
	String!
	✅
	Updated by
	tes
	String!
	✅
	tes
	employeeId
	String!
	✅
	Employee ID
	files
	[EmploymentProofFile!]!
	✅
	List of employment proof files
	subTitle
	String
	

	Subtitle (optional)
	recordIdentifier
	String!
	✅
	Record identifier
	

Nested Type: EmploymentProofFile


Field
	Type
	Required
	Description
	fileUrl
	String!
	✅
	File URL
	fileContent
	String!
	✅
	File content (base64/URL)
	originalFilename
	String!
	✅
	riginal file name
	createdBy
	String!
	✅
	Created by
	updatedBy
	String!
	✅
	Updated by
	createdAt
	String!
	✅
	Created at
	updatedAt
	String!
	✅
	Updated at
	id
	Int!
	✅
	File ID
	

 API: getAllEmployment
🔸 Request Payload


Parameter
	Type
	Required
	Description
	userId
	String!
	✅
	User's unique identifier
	page
	Int!
	✅
	Page number (pagination)
	limit
	Int!
	✅
	Number of records per page
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Response message
	success
	Boolean!
	✅
	Indicates if the request was successful
	code
	Int!
	✅
	Status code of the response
	error
	String
	

	Error message if any
	employment
	[Employment!]!
	✅
	List of employment records
	totalPages
	Int!
	✅
	Total number of pages
	totalRecords
	Int!
	✅
	Total number of records
	currentPage
	Int!
	✅
	Current page number
	

Nested Type: Employment


Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID
	userId
	String!
	✅
	User's unique identifier
	employmentTypeId
	Int!
	✅
	Employment type ID
	employmentType
	String!
	✅
	Employment type name
	companyName
	String!
	✅
	Company name
	designation
	String!
	✅
	Designation
	salaryRangeId
	Int!
	✅
	Salary range ID
	salaryRange
	String!
	✅
	Salary range label
	typefEmploymentId
	Int!
	✅
	Type of employment ID
	typefEmployment
	String!
	✅
	Type of employment name
	streetNameAndNumber
	String!
	✅
	Street address
	apartmentUnitNumber
	String!
	✅
	Apartment/unit number
	city
	String!
	✅
	City
	state
	String!
	✅
	State
	country
	String!
	✅
	Country
	pincode
	String!
	✅
	Pincode
	currentEmployment
	Boolean!
	✅
	Is this the current employment
	startDate
	String!
	✅
	Start date
	endDate
	String!
	✅
	End date
	createdAt
	String!
	✅
	Created at
	updatedAt
	String!
	✅
	Updated at
	createdBy
	String!
	✅
	Created by
	updatedBy
	String!
	✅
	Updated by
	tes
	String!
	✅
	tes
	employeeId
	String!
	✅
	Employee ID
	files
	[EmploymentProofFile!]!
	✅
	List of employment proof files
	subTitle
	String
	

	Subtitle (optional)
	recordIdentifier
	String!
	✅
	Record identifier
	

Nested Type: EmploymentProofFile


Field
	Type
	Required
	Description
	fileUrl
	String!
	✅
	File URL
	fileContent
	String!
	✅
	File content (base64/URL)
	originalFilename
	String!
	✅
	riginal file name
	createdBy
	String!
	✅
	Created by
	updatedBy
	String!
	✅
	Updated by
	createdAt
	String!
	✅
	Created at
	updatedAt
	String!
	✅
	Updated at
	id
	Int!
	✅
	File ID
	

 API: getDashboard
🔸 Request Payload


Parameter
	Type
	Required
	Description
	input
	Dashboardinput!
	✅
	Dashboard input object
	Nested Type: Dashboardinput


Field
	Type
	Required
	Description
	userId
	String!
	✅
	User's unique identifier
	vaultId
	Int!
	✅
	Vault ID
	🔸 Response Fields


Field
	Type
	Required
	Description
	submodules
	[VaultAndGroups]
	

	List of vault submodules and groups
	message
	String
	

	Response message
	code
	Int
	

	Status code of the response
	success
	Boolean
	

	Indicates if the request was successful
	

 API: getAddressDependentsByUserId
🔸 Request Payload


Parameter
	Type
	Required
	Description
	userId
	String!
	✅
	User's unique identifier
	currentRelation
	Boolean
	

	Filter by current relation (optional)
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	message
	String
	

	Response message
	code
	Int!
	✅
	Status code of the response
	success
	Boolean
	

	Indicates if the request was successful
	error
	String
	

	Error message if any
	data
	[AddressDependentsDetails]
	

	List of address dependents details
	

Nested Type: AddressDependentsDetails


Field Name
	Type
	Required
	Description
	id
	Int!
	✅
	Unique ID
	relationId
	Int!
	✅
	Relation ID
	partnerName
	String
	

	Partner name
	dependentName
	[String]
	

	List of dependent names
	name
	[String]
	

	List of names
	date
	String
	

	Date
	relationshipName
	String
	

	Relationship name
	recordIdentifier
	String!
	✅
	Record identifier
	

 API: getAddressDependentsById
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	R
	The unique identifier of the user.
	id
	Int
	R
	The address ID to fetch dependents for
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	R
	Status code of the response.
	success
	Boolean
	R
	Indicates if the request was successful.
	message
	String
	R
	Informational message about the response.
	error
	String
	

	Error message if the request failed.
	data
	[GetRelationAndDependents!]
	R
	List of dependents and their relation details.
	

Nested Type: GetRelationAndDependents


Field Name
	Type
	Required
	Description
	id
	Int
	R
	Dependent's unique identifier.
	userId
	String
	R
	User ID associated with dependent.
	type
	String
	R
	Type of relation.
	typeId
	Int
	R
	Type ID of the relation.
	typeName
	String
	

	Name of the relation type.
	

API: printPdf
🔸 Request Payload
Field Name
	Type
	Required
	Description
	userId
	String
	R
	The unique identifier of the user.
	id
	Int
	R
	The address ID to fetch dependents for.
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	R
	Status code of the response.
	success
	Boolean
	R
	Indicates if the request was successful.
	message
	String
	R
	Informational message about the response.
	error
	String
	

	Error message if the request failed.
	data
	[GetRelationAndDependents!]
	R
	List of dependents and their relation details.
	

Nested Type: GetRelationAndDependents


Field Name
	Type
	Required
	Description
	id
	Int
	R
	Dependent's unique identifier.
	userId
	String
	R
	User ID associated with dependent.
	type
	String
	R
	Type of relation.
	typeId
	Int
	R
	Type ID of the relation.
	typeName
	String
	

	Name of the relation type.
	

 API: emergencyContactBreclate
🔸 Request Payload


Field Name
	Type
	Required
	Description
	userId
	String
	R
	The unique identifier of the user.
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	R
	Status code of the response.
	emergencyContact
	[EmergencyContactData]
	R
	List of emergency contact details.
	

API: getIndustries
🔸 Request Payload
ne
🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	R
	Status code of the response.
	success
	Boolean
	R
	Indicates if the request succeeded.
	message
	String
	R
	Informational message.
	industries
	[Industries!]
	R
	List of industry objects.
	error
	String
	

	Error message if the request failed.
	

API: getSubCategories
🔸 Request Payload
Field Name
	Type
	Required
	Description
	industryId
	Int
	R
	The ID of the industry to fetch subcategories for.
	🔸 Response Fields


Field Name
	Type
	Required
	Description
	code
	Int
	R
	Status code of the response.
	success
	Boolean
	R
	Indicates if the request succeeded.
	message
	String
	R
	Informational message.
	subCategories
	[SubCategory!]
	R
	List of subcategory objects.
	error
	String
	

	Error message if the request failed.
	

Nested Type: SubCategory


Field Name
	Type
	Required
	Description
	id
	Int
	R
	Subcategory unique identifier.
	categoryId
	Int
	R
	Parent category ID.
	name
	String
	R
	Name of the subcategory.
	



 API: getCertificationStatuses
🔸 Request Payload
ne
🔸 Response Fields


Field Name
	Type
	Required
	Description
	statuses
	[CertificationStatus!]
	R
	List of certification status objects.
	code
	Int
	R
	Status code of the response.
	success
	Boolean
	R
	Indicates if the request succeeded.
	message
	String
	R
	Informational message.
	error
	String
	R
	Error message if the request failed.
	

Nested Type: CertificationStatus


Field Name
	Type
	Required
	Description
	id
	ID
	R
	Unique identifier for the status.
	status
	String
	R
	Name of the certification status.
	

API: getProficiencyLevels
🔸 Request Payload
ne
🔸 Response Fields


Field Name
	Type
	Required
	Description
	statuses
	[CertificationStatus!]
	R
	List of certification status objects.
	code
	Int
	R
	Status code of the response.
	success
	Boolean
	R
	Indicates if the request succeeded.
	message
	String
	R
	Informational message.
	error
	String
	R
	Error message if the request failed.
	

Nested Type: CertificationStatus
Field Name
	Type
	Required
	Description
	id
	ID
	R
	Unique identifier for the status.
	status
	String
	R
	Name of the certification status.
	

 API: createRelationshipStatus
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String!
	✅
	User's unique identifier
	relationshipTypeId
	Int!
	✅
	Relationship type ID
	relationshipStatus
	String!
	✅
	Status of the relationship
	isCurrentRelationship
	Boolean!
	✅
	Is this the current relationship
	startDate
	String!
	✅
	Start date
	endDate
	String
	

	End date (optional)
	tes
	String
	

	tes (optional)
	createdBy
	String
	

	Created by (optional)
	files
	[RelationshipStatusFileInput!]!
	✅
	List of relationship status files
	othersValue
	String
	

	ther value (optional)
	

Nested Type: RelationshipStatusFileInput


Field
	Type
	Required
	Description
	originalFilename
	String!
	✅
	riginal file name
	file
	Upload!
	✅
	File upload
	userId
	String!
	✅
	User's unique identifier
	createdBy
	String
	

	Created by (optional)
	action
	String!
	✅
	Action type
	updatedBy
	String
	

	Updated by (optional)
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Response message
	success
	Boolean!
	✅
	Indicates if the request was successful
	code
	Int!
	✅
	Status code of the response
	error
	String
	

	Error message if any
	

 API: updateRelationshipStatus
🔸 Request Payload


Parameter
	Type
	Required
	Description
	input
	UpdateRelationshipStatusInput!
	✅
	Relationship status input
	

Nested Type: UpdateRelationshipStatusInput


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Relationship status record ID
	userId
	String!
	✅
	User's unique identifier
	relationshipTypeId
	Int!
	✅
	Relationship type ID
	relationshipStatus
	String!
	✅
	Status of the relationship
	isCurrentRelationship
	Boolean!
	✅
	Is this the current relationship
	startDate
	String!
	✅
	Start date
	endDate
	String
	

	End date (optional)
	tes
	String
	

	tes (optional)
	updatedBy
	String
	

	Updated by (optional)
	files
	[RelationshipStatusFileInput!]!
	✅
	List of relationship status files
	othersValue
	String
	

	ther value (optional)
	

Nested Type: RelationshipStatusFileInput


Field
	Type
	Required
	Description
	originalFilename
	String!
	✅
	riginal file name
	file
	Upload!
	✅
	File upload
	userId
	String!
	✅
	User's unique identifier
	createdBy
	String
	

	Created by (optional)
	action
	String!
	✅
	Action type
	updatedBy
	String
	

	Updated by (optional)
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Response message
	success
	Boolean!
	✅
	Indicates if the request was successful
	code
	Int!
	✅
	Status code of the response
	error
	String
	

	Error message if any
	

 API: deleteRelationshipStatus
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	ID of the relationship status to delete
	updatedBy
	String
	✅
	User ID or identifier of the person performing the deletion
	userId
	String
	✅
	User ID to whom the relationship status belongs
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Human-readable message about the operation
	success
	Boolean
	✅
	Indicates if the deletion was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	

 API: addIdentityProof
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to whom the identity proof belongs
	identityProofTypeId
	Int
	✅
	Type ID of the identity proof
	nationality
	String
	

	Nationality of the user
	documentNumber
	String
	✅
	Document number of the identity proof
	files
	[AddFileInput!]
	✅
	List of files to upload (see below)
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload
	✅
	File to upload
	originalFilename
	String
	✅
	riginal name of the file
	🔸 Response Fields


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	identityProofTypeId
	Int
	✅
	Type ID of the identity proof
	nationality
	String
	

	Nationality of the user
	documentNumber
	String
	✅
	Document number
	id
	Int
	✅
	ID of the created identity proof
	files
	[FileType!]
	✅
	List of uploaded files (see below)
	message
	String
	✅
	Human-readable message
	success
	Boolean
	✅
	Indicates if the operation was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	recordIdentifier
	String
	✅
	Unique identifier for the record
	

API: updateIdentityProof
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	ID of the identity proof to update
	userId
	String
	✅
	User ID to whom the identity proof belongs
	identityProofTypeId
	Int
	✅
	Type ID of the identity proof
	nationality
	String
	

	Nationality of the user
	documentNumber
	String
	✅
	Document number of the identity proof
	action
	String
	✅
	Action to perform (e.g., update, replace)
	files
	[UpdateIdentityFileInput!]
	✅
	List of files to upload/update (see below)
	

Nested Type: UpdateIdentityFileInput!


Field Name
	Type
	Required
	Description
	id
	Int
	

	File ID (for update)
	file
	Upload
	✅
	File to upload
	originalFilename
	String
	✅
	riginal name of the file
	🔸 Response Fields


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	identityProofTypeId
	Int
	✅
	Type ID of the identity proof
	nationality
	String
	

	Nationality of the user
	documentNumber
	String
	✅
	Document number
	id
	Int
	✅
	ID of the updated identity proof
	files
	[FileType!]
	✅
	List of uploaded files (see below)
	message
	String
	✅
	Human-readable message
	success
	Boolean
	✅
	Indicates if the operation was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	recordIdentifier
	String
	✅
	Unique identifier for the record
	

 API: deleteIdentityProof
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	ID of the identity proof to delete
	userId
	String
	✅
	User ID to whom the identity proof belongs
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Human-readable message about the operation
	success
	Boolean
	✅
	Indicates if the deletion was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	 API: addDependent
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to whom the dependent belongs
	dependentTypeId
	Int
	✅
	Type ID of the dependent
	dependentName
	String
	

	Name of the dependent
	dob
	String
	✅
	Date of birth of the dependent
	tes
	String
	✅
	tes about the dependent
	others
	String
	✅
	ther information about the dependent
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Human-readable message about the operation
	success
	Boolean
	✅
	Indicates if the operation was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	

 API: deleteDependent
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	ID of the dependent to delete
	userId
	String
	✅
	User ID to whom the dependent belongs
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Human-readable message about the operation
	success
	Boolean
	✅
	Indicates if the deletion was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	

 API: updateDependent
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	ID of the dependent to update
	userId
	String
	✅
	User ID to whom the dependent belongs
	dependentTypeId
	Int
	✅
	Type ID of the dependent
	dependentName
	String
	

	Name of the dependent
	dob
	String
	✅
	Date of birth of the dependent
	tes
	String
	✅
	tes about the dependent
	others
	String
	✅
	ther information about the dependent
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Human-readable message about the operation
	success
	Boolean
	✅
	Indicates if the operation was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	

API: addAddressDetails
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to whom the address belongs
	addressTypeId
	Int
	✅
	Type ID of the address
	streetNameAndNumber
	String
	✅
	Street name and number
	apartmentUnitNumber
	String
	✅
	Apartment/unit number
	city
	String
	✅
	City
	state
	String
	✅
	State
	country
	String
	✅
	Country
	pincode
	String
	✅
	Postal code
	isCurrentAddress
	Boolean
	✅
	Is this the current address?
	startDate
	String
	

	Start date of residence
	endDate
	String
	

	End date of residence
	othersValue
	String
	

	ther information
	companyName
	String
	

	Company name (if applicable)
	files
	[AddFileInput]
	

	List of files to upload (see below)
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload
	✅
	File to upload
	originalFilename
	String
	✅
	riginal name of the file
	🔸 Response Fields


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	addressTypeId
	Int
	✅
	Type ID of the address
	streetNameAndNumber
	String
	✅
	Street name and number
	apartmentUnitNumber
	String
	✅
	Apartment/unit number
	city
	String
	✅
	City
	state
	String
	✅
	State
	country
	String
	✅
	Country
	pincode
	String
	✅
	Postal code
	isCurrentAddress
	Boolean
	✅
	Is this the current address?
	startDate
	String
	✅
	Start date of residence
	endDate
	String
	✅
	End date of residence
	othersValue
	String
	

	ther information
	files
	[FileType!]
	✅
	List of uploaded files (see below)
	id
	Int
	✅
	ID of the created address
	message
	String
	✅
	Human-readable message
	success
	Boolean
	✅
	Indicates if the operation was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	recordIdentifier
	String
	✅
	Unique identifier for the record
	

 API: updateAddressDetails
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	ID of the address to update
	userId
	String
	✅
	User ID to whom the address belongs
	addressTypeId
	Int
	✅
	Type ID of the address
	streetNameAndNumber
	String
	✅
	Street name and number
	apartmentUnitNumber
	String
	✅
	Apartment/unit number
	city
	String
	✅
	City
	state
	String
	✅
	State
	country
	String
	✅
	Country
	pincode
	String
	✅
	Postal code
	isCurrentAddress
	Boolean
	✅
	Is this the current address?
	startDate
	String
	

	Start date of residence
	endDate
	String
	

	End date of residence
	othersValue
	String
	

	ther information
	companyName
	String
	

	Company name (if applicable)
	files
	[AddFileInput]
	

	List of files to upload (see below)
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload
	✅
	File to upload
	originalFilename
	String
	✅
	riginal name of the file
	🔸 Response Fields


Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	addressTypeId
	Int
	✅
	Type ID of the address
	streetNameAndNumber
	String
	✅
	Street name and number
	apartmentUnitNumber
	String
	✅
	Apartment/unit number
	city
	String
	✅
	City
	state
	String
	✅
	State
	country
	String
	✅
	Country
	pincode
	String
	✅
	Postal code
	isCurrentAddress
	Boolean
	✅
	Is this the current address?
	startDate
	String
	✅
	Start date of residence
	endDate
	String
	✅
	End date of residence
	othersValue
	String
	

	ther information
	files
	[FileType!]
	✅
	List of uploaded files (see below)
	id
	Int
	✅
	ID of the updated address
	message
	String
	✅
	Human-readable message
	success
	Boolean
	✅
	Indicates if the operation was successful
	code
	Int
	✅
	Status or error code
	error
	String
	

	Error message if the operation failed
	recordIdentifier
	String
	✅
	Unique identifier for the record
	

 API: deleteAddressDetails
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the address
	userId
	String
	✅
	User's unique identifier
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	peration status message
	success
	Boolean
	✅
	Indicates if deletion succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	

API: createEducation
🔸 Request Payload


Field
	Type
	Required
	Description
	educationCertificateId
	Int
	

	Certificate ID
	educationCertificateName
	String
	✅
	Certificate name
	nameAsPerCertificate
	String
	✅
	Name as per certificate
	universityrCollegeName
	String
	✅
	University or college name
	roll
	String
	

	Roll number
	completionYear
	Int
	

	Year of completion
	isCurrentlyPursuing
	Boolean
	✅
	Is currently pursuing
	startDate
	String
	

	Start date
	endDate
	String
	

	End date
	userId
	String
	✅
	User's unique identifier
	createdBy
	String
	✅
	Created by
	others
	String
	✅
	ther information
	files
	[AddFileInput!]
	✅
	List of files (upload)
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload
	✅
	The file to be uploaded
	originalFilename
	String
	✅
	riginal name of the file
	🔸 Response Fields


Field
	Type
	Required
	Description
	educationCertificateId
	Int
	

	Certificate ID
	educationCertificateName
	String
	✅
	Certificate name
	nameAsPerCertificate
	String
	✅
	Name as per certificate
	universityrCollegeName
	String
	✅
	University or college name
	roll
	String
	

	Roll number
	completionYear
	Int
	

	Year of completion
	isCurrentlyPursuing
	Boolean
	✅
	Is currently pursuing
	startDate
	String
	

	Start date
	endDate
	String
	

	End date
	userId
	String
	✅
	User's unique identifier
	createdBy
	String
	✅
	Created by
	others
	String
	✅
	ther information
	id
	Int
	✅
	Education record ID
	files
	[FileType!]
	✅
	List of uploaded files
	message
	String
	✅
	peration status message
	success
	Boolean
	✅
	Indicates if creation succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	recordIdentifier
	String
	✅
	Unique record identifier
	

Nested Type: FileType


Field
	Type
	Required
	Description
	file
	Upload
	✅
	The file to be uploaded
	originalFilename
	String
	✅
	riginal name of the file
	

 API: updateEducation
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int
	✅
	Education record ID
	educationCertificateId
	Int
	

	Certificate ID
	educationCertificateName
	String
	✅
	Certificate name
	nameAsPerCertificate
	String
	✅
	Name as per certificate
	universityrCollegeName
	String
	✅
	University or college name
	roll
	String
	

	Roll number
	completionYear
	Int
	

	Year of completion
	isCurrentlyPursuing
	Boolean
	✅
	Is currently pursuing
	startDate
	String
	

	Start date
	endDate
	String
	

	End date
	userId
	String
	✅
	User's unique identifier
	updatedBy
	String
	✅
	Updated by
	others
	String
	✅
	ther information
	files
	[AddFileInput!]
	✅
	List of files (upload)
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload
	✅
	The file to be uploaded
	originalFilename
	String
	✅
	riginal name of the file
	

🔸 Response Fields


Field
	Type
	Required
	Description
	educationCertificateId
	Int
	

	Certificate ID
	educationCertificateName
	String
	✅
	Certificate name
	nameAsPerCertificate
	String
	✅
	Name as per certificate
	universityrCollegeName
	String
	✅
	University or college name
	roll
	String
	

	Roll number
	completionYear
	Int
	

	Year of completion
	isCurrentlyPursuing
	Boolean
	✅
	Is currently pursuing
	startDate
	String
	

	Start date
	endDate
	String
	

	End date
	userId
	String
	✅
	User's unique identifier
	createdBy
	String
	✅
	Created by
	others
	String
	✅
	ther information
	id
	Int
	✅
	Education record ID
	files
	[FileType!]
	✅
	List of uploaded files
	message
	String
	✅
	peration status message
	success
	Boolean
	✅
	Indicates if update succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	recordIdentifier
	String
	✅
	Unique record identifier
	

Nested Type: FileType


Field
	Type
	Required
	Description
	id
	Int
	✅
	File record ID
	documentFileLink
	String
	✅
	Link to the uploaded file
	originalFileName
	String
	✅
	riginal name of the file
	createdBy
	String
	✅
	Who uploaded the file
	updatedBy
	String
	✅
	Who last updated the file
	createdAt
	String
	✅
	Creation timestamp
	updatedAt
	String
	✅
	Last update timestamp
	



API: deleteEducationById
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the education record
	userId
	String
	✅
	User's unique identifier
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	peration status message
	success
	Boolean
	✅
	Indicates if deletion succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	

API: createContact
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	User's unique identifier
	contactTypeId
	[Int!]
	✅
	List of contact type IDs
	name
	String
	✅
	Contact name
	contactNumber
	String
	

	Contact number
	companyName
	String
	

	Company name
	employeeId
	String
	

	Employee ID
	relationship
	String
	

	Relationship
	emailId
	String
	

	Email ID
	streetNameAndNumber
	String
	

	Street name and number
	apartmentNumber
	String
	

	Apartment number
	city
	String
	

	City
	state
	String
	

	State
	pincode
	String
	

	Pincode
	country
	String
	

	Country
	createdBy
	String
	✅
	Created by
	relationId
	Int
	

	Relation ID
	thers
	String
	

	ther information
	jobRole
	String
	

	Job role
	dob
	String
	

	Date of birth
	isDeceased
	Boolean
	

	Is deceased
	datefDeath
	String
	

	Date of death
	🔸 Response Fields


Field
	Type
	Required
	Description
	id
	Int
	✅
	Contact record ID
	userId
	String
	✅
	User's unique identifier
	contactTypeId
	[Int!]
	✅
	List of contact type IDs
	name
	String
	✅
	Contact name
	contactNumber
	String
	

	Contact number
	companyName
	String
	

	Company name
	employeeId
	String
	

	Employee ID
	relationship
	String
	

	Relationship
	emailId
	String
	

	Email ID
	streetNameAndNumber
	String
	

	Street name and number
	apartmentNumber
	String
	

	Apartment number
	city
	String
	

	City
	state
	String
	

	State
	pincode
	String
	

	Pincode
	country
	String
	

	Country
	createdBy
	String
	✅
	Created by
	relationId
	Int
	

	Relation ID
	thers
	String
	

	ther information
	jobRole
	String
	

	Job role
	message
	String
	✅
	peration status message
	success
	Boolean
	✅
	Indicates if creation succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	recordIdentifier
	String
	✅
	Unique record identifier
	dob
	String
	

	Date of birth
	isDeceased
	Boolean
	

	Is deceased
	datefDeath
	String
	

	Date of death
	

 API: updateContact
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	Contact record ID
	userId
	String
	✅
	User's unique identifier
	contactTypeId
	[Int!]
	✅
	List of contact type IDs
	name
	String
	✅
	Contact name
	contactNumber
	String
	

	Contact number
	companyName
	String
	

	Company name
	employeeId
	String
	

	Employee ID
	relationship
	String
	

	Relationship
	emailId
	String
	

	Email ID
	streetNameAndNumber
	String
	

	Street name and number
	apartmentNumber
	String
	

	Apartment number
	city
	String
	

	City
	state
	String
	

	State
	pincode
	String
	

	Pincode
	country
	String
	

	Country
	updatedBy
	String
	✅
	Updated by
	relationId
	Int
	

	Relation ID
	thers
	String
	

	ther information
	dob
	String
	

	Date of birth
	isDeceased
	Boolean
	

	Is deceased
	datefDeath
	String
	

	Date of death
	jobRole
	String
	

	Job role
	🔸 Response Fields


Field
	Type
	Required
	Description
	id
	Int
	✅
	Contact record ID
	userId
	String
	✅
	User's unique identifier
	contactTypeId
	[Int!]
	✅
	List of contact type IDs
	name
	String
	✅
	Contact name
	contactNumber
	String
	

	Contact number
	companyName
	String
	

	Company name
	employeeId
	String
	

	Employee ID
	relationship
	String
	

	Relationship
	emailId
	String
	

	Email ID
	streetNameAndNumber
	String
	

	Street name and number
	apartmentNumber
	String
	

	Apartment number
	city
	String
	

	City
	state
	String
	

	State
	pincode
	String
	

	Pincode
	country
	String
	

	Country
	createdBy
	String
	✅
	Created by
	relationId
	Int
	

	Relation ID
	thers
	String
	

	ther information
	jobRole
	String
	

	Job role
	message
	String
	✅
	peration status message
	success
	Boolean
	✅
	Indicates if update succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	recordIdentifier
	String
	✅
	Unique record identifier
	dob
	String
	

	Date of birth
	isDeceased
	Boolean
	

	Is deceased
	datefDeath
	String
	

	Date of death
	

 API: deleteContact
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	[Int!]!
	✅
	List of contact IDs to delete
	userId
	String!
	✅
	User ID for whom contacts are deleted
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if deletion succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	

API: addEmployment
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String!
	✅
	User ID for whom employment is added
	employmentTypeId
	Int!
	✅
	Employment type ID
	companyName
	String
	

	Name of the company
	designation
	String
	

	Job designation
	salaryRangeId
	Int
	

	Salary range ID
	typefEmploymentId
	Int
	

	Type of employment ID
	streetNameAndNumber
	String
	

	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String
	

	City
	state
	String
	

	State
	country
	String
	

	Country
	pincode
	String
	

	Postal code
	currentEmployment
	Boolean
	

	Is this the current employment?
	startDate
	String
	

	Employment start date
	endDate
	String
	

	Employment end date
	othersValue
	String
	

	ther value (custom field)
	tes
	String
	

	Additional tes
	employeeId
	String
	

	Employee ID
	createdBy
	String
	

	Creator's identifier
	files
	[AddFileInput!]!
	✅
	List of files to upload
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload!
	✅
	File to upload
	originalFilename
	String!
	✅
	riginal file name
	🔸 Response Fields


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID
	userId
	String!
	✅
	User ID
	employmentTypeId
	Int!
	✅
	Employment type ID
	companyName
	String
	

	Name of the company
	designation
	String
	

	Job designation
	salaryRangeId
	Int
	

	Salary range ID
	typefEmploymentId
	Int
	

	Type of employment ID
	streetNameAndNumber
	String
	

	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String
	

	City
	state
	String
	

	State
	country
	String
	

	Country
	pincode
	String
	

	Postal code
	currentEmployment
	Boolean
	

	Is this the current employment?
	startDate
	String
	

	Employment start date
	endDate
	String
	

	Employment end date
	othersValue
	String
	

	ther value (custom field)
	tes
	String
	

	Additional tes
	employeeId
	String
	

	Employee ID
	createdBy
	String
	

	Creator's identifier
	files
	[FileType!]!
	✅
	List of uploaded files
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if addition succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	recordIdentifier
	String!
	✅
	Unique record identifier
	

 API: updateEmployment
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID to update
	userId
	String!
	✅
	User ID for whom employment is updated
	employmentTypeId
	Int!
	✅
	Employment type ID
	companyName
	String
	

	Name of the company
	designation
	String
	

	Job designation
	salaryRangeId
	Int
	

	Salary range ID
	typefEmploymentId
	Int
	

	Type of employment ID
	streetNameAndNumber
	String
	

	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String
	

	City
	state
	String
	

	State
	country
	String
	

	Country
	pincode
	String
	

	Postal code
	currentEmployment
	Boolean
	

	Is this the current employment?
	startDate
	String
	

	Employment start date
	endDate
	String
	

	Employment end date
	othersValue
	String
	

	ther value (custom field)
	tes
	String
	

	Additional tes
	employeeId
	String
	

	Employee ID
	updatedBy
	String
	

	Updater's identifier
	files
	[AddFileInput!]!
	✅
	List of files to upload
	

Nested Type: AddFileInput


Field
	Type
	Required
	Description
	file
	Upload!
	✅
	File to upload
	originalFilename
	String!
	✅
	riginal file name
	🔸 Response Fields


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID
	userId
	String!
	✅
	User ID
	employmentTypeId
	Int!
	✅
	Employment type ID
	companyName
	String
	

	Name of the company
	designation
	String
	

	Job designation
	salaryRangeId
	Int
	

	Salary range ID
	typefEmploymentId
	Int
	

	Type of employment ID
	streetNameAndNumber
	String
	

	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String
	

	City
	state
	String
	

	State
	country
	String
	

	Country
	pincode
	String
	

	Postal code
	currentEmployment
	Boolean
	

	Is this the current employment?
	startDate
	String
	

	Employment start date
	endDate
	String
	

	Employment end date
	othersValue
	String
	

	ther value (custom field)
	tes
	String
	

	Additional tes
	employeeId
	String
	

	Employee ID
	createdBy
	String
	

	Creator's identifier
	files
	[FileType!]!
	✅
	List of uploaded files
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if update succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	recordIdentifier
	String!
	✅
	Unique record identifier
	

API: deleteEmployment
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Employment record ID to delete
	userId
	String!
	✅
	User ID for whom employment is deleted
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if deletion succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	

API: addRelationAndDependents
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String!
	✅
	User ID for whom relation/dependent is added
	type
	String!
	✅
	Type identifier (relation/dependent)
	typeId
	Int!
	✅
	Type ID
	streetNameAndNumber
	String!
	✅
	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String!
	✅
	City
	state
	String!
	✅
	State
	country
	String!
	✅
	Country
	pincode
	String!
	✅
	Postal code
	isCurrentRelation
	Boolean!
	✅
	Is this the current relation?
	startDate
	String
	

	Relation start date
	endDate
	String
	

	Relation end date
	othersValue
	String
	

	ther value (custom field)
	files
	[FileRequestInput!]
	

	List of files to upload
	name
	String!
	✅
	Name of relation/dependent
	dob
	String!
	✅
	Date of birth
	age
	String!
	✅
	Age
	dependentStatus
	String!
	✅
	Dependent status
	emailId
	String!
	✅
	Email address
	phoneNumber
	String!
	✅
	Phone number
	gender
	String!
	✅
	Gender
	contactId
	Int!
	✅
	Contact ID
	tes
	String
	

	Additional tes
	typeName
	String!
	✅
	Type name
	

Nested Type: FileRequestInput


Field
	Type
	Required
	Description
	file
	Upload!
	✅
	File to upload
	originalFilename
	String!
	✅
	riginal file name
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if addition succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	data
	[AddRelationAndDependentsutput!]
	✅
	List of added records
	Nested Type: AddRelationAndDependentsutput


Field
	Type
	Required
	Description
	id
	Int!
	✅
	Record ID
	userId
	String!
	✅
	User ID
	type
	String!
	✅
	Type identifier
	typeId
	Int!
	✅
	Type ID
	streetNameAndNumber
	String!
	✅
	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String!
	✅
	City
	state
	String!
	✅
	State
	country
	String!
	✅
	Country
	pincode
	String!
	✅
	Postal code
	isCurrentRelation
	Boolean!
	✅
	Is this the current relation?
	startDate
	String
	

	Relation start date
	endDate
	String
	

	Relation end date
	othersValue
	String
	

	ther value (custom field)
	files
	[FileType!]
	

	List of uploaded files
	name
	String!
	✅
	Name of relation/dependent
	dob
	String!
	✅
	Date of birth
	age
	String!
	✅
	Age
	dependentStatus
	String!
	✅
	Dependent status
	emailId
	String!
	✅
	Email address
	phoneNumber
	String!
	✅
	Phone number
	gender
	String!
	✅
	Gender
	contactId
	Int!
	✅
	Contact ID
	tes
	String
	

	Additional tes
	typeName
	String!
	✅
	Type name
	recordIdentifier
	String!
	✅
	Unique record identifier
	

API: updateRelationAndDependents
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	ID!
	✅
	User ID for whom relation/dependent is updated
	type
	String!
	✅
	Type identifier (relation/dependent)
	typeId
	Int
	

	Type ID
	streetNameAndNumber
	String
	

	Street address
	apartmentUnitNumber
	String
	

	Apartment/unit number
	city
	String
	

	City
	state
	String
	

	State
	country
	String
	

	Country
	pincode
	String
	

	Postal code
	isCurrentRelation
	Boolean
	

	Is this the current relation?
	startDate
	String
	

	Relation start date
	endDate
	String
	

	Relation end date
	othersValue
	String
	

	ther value (custom field)
	files
	[FileDetailsInput]
	

	List of files to upload
	name
	String
	

	Name of relation/dependent
	dob
	String
	

	Date of birth
	emailId
	String
	

	Email address
	phoneNumber
	String
	

	Phone number
	gender
	String
	

	Gender
	contactId
	Int
	

	Contact ID
	tes
	String
	

	Additional tes
	typeName
	String
	

	Type name
	relationName
	String
	

	Relation name
	id
	Int
	

	Record ID
	age
	String
	

	Age
	dependentStatus
	String
	

	Dependent status
	actualId
	Int
	

	Actual ID
	

Nested Type: FileDetailsInput


Field
	Type
	Required
	Description
	id
	Int
	

	File ID
	originalFilename
	String
	

	riginal file name
	relationId
	Int
	

	Relation ID
	documentLink
	String
	

	Document link
	file
	Upload
	

	File to upload
	🔸 Response Fields


Field
	Type
	Required
	Description
	code
	Int!
	✅
	Status code
	success
	Boolean!
	✅
	Indicates if update succeeded
	message
	String!
	✅
	Status or result message
	error
	String
	

	Error message if any
	

API: deleteFilesRD
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int!
	✅
	File ID to delete
	userId
	String!
	✅
	User ID for whom the file is deleted
	type
	String!
	✅
	Type of file (relation/dependent)
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if deletion succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	

API: deleteRelationDependents
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int!
	✅
	ID of the relation/dependent to delete
	🔸 Response Fields


Field
	Type
	Required
	Description
	message
	String!
	✅
	Status or result message
	success
	Boolean!
	✅
	Indicates if deletion succeeded
	code
	Int!
	✅
	Status code
	error
	String
	

	Error message if any
	

API: deleteRelationDependentsById
🔸 Request Payload


Name
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier of the relation/dependent
	userId
	String
	✅
	User’s unique identifier
	type
	String
	✅
	Type of record ("relation" or "dependent")
	🔸 Response Fields


Name
	Type
	Required
	Description
	message
	String
	✅
	Status message
	success
	Boolean
	✅
	Indicates if deletion was successful
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if operation failed
	

 API: fileReUpload
🔸 Request Payload


Name
	Type
	Required
	Description
	id
	Int
	

	File record identifier
	Filename
	String
	

	Name of the file
	userId
	String
	

	User’s unique identifier
	fileContent
	Upload
	

	The new file content to upload
	type
	String
	

	Type of file (context-specific)
	🔸 Response Fields


Name
	Type
	Required
	Description
	message
	String
	✅
	Status message
	success
	Boolean
	✅
	Indicates if upload was successful
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if operation failed
	fileName
	String
	

	Name of the uploaded file
	fileContent
	String
	

	Content or link to the uploaded file
	

 API: addSkillSets
🔸 Request Payload


Name
	Type
	Required
	Description
	userId
	String
	✅
	User’s unique identifier
	industrySkillSets
	[IndustrySkillSetInput!]
	✅
	List of industry skill sets to add
	Nested Type: IndustrySkillSetInput


Name
	Type
	Required
	Description
	industryId
	Int
	✅
	Industry identifier
	industry
	String
	✅
	Industry name
	categories
	[CategorySkillSetInput!]
	✅
	List of skill categories
	

Nested Type: CategorySkillSetInput


Name
	Type
	Required
	Description
	categoryId
	Int
	✅
	Category identifier
	categoryName
	String
	✅
	Category name
	skills
	[SkillInput!]
	✅
	List of skills
	

Nested Type: SkillInput


Name
	Type
	Required
	Description
	skillId
	Int
	✅
	Skill identifier
	skillName
	String
	✅
	Skill name
	certificationStatusId
	Int
	✅
	Certification status ID
	certificationStatus
	String
	✅
	Certification status
	certificationName
	String
	✅
	Certification name
	proficiencyId
	Int
	✅
	Proficiency level ID
	proficiency
	String
	✅
	Proficiency level
	experienceYears
	Int
	✅
	Years of experience
	experienceMonths
	Int
	✅
	Months of experience
	tes
	String
	✅
	Additional tes
	files
	[SkillFileInput]
	

	List of skill files
	

Nested Type: SkillFileInput


Name
	Type
	Required
	Description
	originalFilename
	String
	✅
	Name of the file
	file
	Upload
	✅
	File to upload
	🔸 Response Fields


Name
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Indicates if addition was successful
	message
	String
	✅
	Status message
	error
	String
	

	Error message if operation failed
	skills
	[AddedSkill!]
	✅
	List of added skills
	

Nested Type: AddedSkill


Name
	Type
	Required
	Description
	id
	Int
	✅
	Added skill ID
	recordIdentifier
	String
	✅
	Unique record ID
	

 API: deleteSkillSet
🔸 Request Payload
Name
	Type
	Required
	Description
	userId
	String
	✅
	User’s unique identifier
	industryId
	Int
	✅
	Industry identifier
	categoryId
	Int
	✅
	Skill category identifier
	skillId
	Int
	✅
	Skill identifier to delete
	🔸 Response Fields


Name
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Indicates if deletion was successful
	message
	String
	✅
	Status message
	error
	String
	

	Error message if operation failed
	













Health Service API Documentation





API: UpdateCountry

Description:Updates the details of a country for a user.
🔸 Request Payload (UpdateCountryRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the update
	id
	Int32
	✅
	Country ID to update
	name
	String
	✅
	New name for the country
	🔸 Response Fields (UpdateCountryResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteCountry

Description:Deletes a country record for a user.
🔸 Request Payload (DeleteCountryRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	id
	Int32
	✅
	Country ID to delete
	🔸 Response Fields (DeleteCountryResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateCountry

Description:Creates a new country record for a user.
🔸 Request Payload (CreateCountryRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the country
	name
	String
	✅
	Name of the country
	createdBy
	String
	 
	Creator's user ID
	updatedBy
	String
	 
	Updater's user ID
	🔸 Response Fields (CreateCountryResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if creation succeeded
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if failed
	________________


API: AddQuestion

Description:Adds a question to a form or section.
🔸 Request Payload (AddQuestionsRequest)
Field
	Type
	Required
	Description
	formId
	Int32
	✅
	Form ID to add question
	sectionId
	Int32
	 
	Section ID (if applicable)
	question
	String
	✅
	Question text
	options
	String
	 
	Options for the question
	createdBy
	String
	✅
	User ID creating the question
	🔸 Response Fields (AddQuestionsResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteState

Description:Deletes a state record for a user.
🔸 Request Payload (DeleteStateRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	stateId
	Int32
	✅
	State ID to delete
	🔸 Response Fields (DeleteStateResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateQuestion

Description:Updates a question in a form or section.
🔸 Request Payload (UpdateQuestionRequest)
Field
	Type
	Required
	Description
	questionId
	Int32
	✅
	Question ID to update
	question
	String
	✅
	Updated question text
	options
	String
	 
	Updated options
	updatedBy
	String
	✅
	User ID updating the question
	🔸 Response Fields (UpdateQuestionResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateForm

Description:Creates a new form.
🔸 Request Payload (CreateFormRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the form
	formName
	String
	✅
	Name of the form
	createdBy
	String
	 
	Creator's user ID
	🔸 Response Fields (CreateFormResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteQuestion

Description:Deletes a question from a form or section.
🔸 Request Payload (DeleteQuestionRequest)
Field
	Type
	Required
	Description
	questionId
	Int32
	✅
	Question ID to delete
	deletedBy
	String
	✅
	User ID performing the delete
	🔸 Response Fields (DeleteQuestionResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: AddState

Description:Adds a new state record.
🔸 Request Payload (AddStateRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID adding the state
	stateName
	String
	✅
	Name of the state
	countryId
	Int32
	✅
	Country ID for the state
	🔸 Response Fields (AddStateResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateForm

Description:Updates an existing form.
🔸 Request Payload (UpdateFormRequest)
Field
	Type
	Required
	Description
	formId
	Int32
	✅
	Form ID to update
	formName
	String
	✅
	Updated form name
	updatedBy
	String
	✅
	User ID updating the form
	🔸 Response Fields (UpdateFormResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UserAhdForm

Description:Fetches the AHD form for a user.
🔸 Request Payload (GetUserAhdFormRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to fetch AHD form
	🔸 Response Fields (GetUserAhdFormResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if fetch succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	form
	String
	 
	Fetched AHD form data
	________________


API: CreateMedicalHistory

Description:Creates a new medical history record for a user.
🔸 Request Payload (CreateMedicalHistoryRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the record
	history
	String
	✅
	Medical history details
	createdBy
	String
	 
	Creator's user ID
	🔸 Response Fields (MedicalHistoryResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateFamilyDoctor

Description:Creates a new family doctor record for a user.
🔸 Request Payload (CreateFamilyDoctorRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the record
	doctorName
	String
	✅
	Name of the family doctor
	contact
	String
	 
	Contact details
	🔸 Response Fields (CreateFamilyDoctorResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateMedicationAllergy

Description:Creates a new medication allergy record for a user.
🔸 Request Payload (CreateMedicationAllergyRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the record
	medication
	String
	✅
	Medication name
	allergy
	String
	✅
	Allergy details
	🔸 Response Fields (CreateMedicationAllergyResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateNote

Description:Creates a new note for a user.
🔸 Request Payload (CreateNoteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the note
	note
	String
	✅
	Note content
	🔸 Response Fields (CreateNoteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateHealthInsurance

Description:Creates a new health insurance record for a user.
🔸 Request Payload (CreateHealthInsuranceRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the record
	insuranceName
	String
	✅
	Name of the insurance
	policyNumber
	String
	✅
	Policy number
	provider
	String
	 
	Insurance provider
	🔸 Response Fields (CreateHealthInsuranceResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________




API: UpdateState

Description:Updates the details of a state for a user.
🔸 Request Payload (UpdateStateRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the update
	id
	Int32
	✅
	State ID to update
	name
	String
	✅
	New name for the state
	🔸 Response Fields (UpdateStateResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteForm

Description:Deletes a form for a user.
🔸 Request Payload (DeleteFormRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	formId
	Int32
	✅
	Form ID to delete
	🔸 Response Fields (DeleteFormResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteMedicalHistory

Description:Deletes a medical history record for a user.
🔸 Request Payload (deleteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	historyId
	Int32
	✅
	Medical history ID to delete
	🔸 Response Fields (deleteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteDoctorDetails

Description:Deletes a doctor details record for a user.
🔸 Request Payload (deleteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	doctorId
	Int32
	✅
	Doctor ID to delete
	🔸 Response Fields (deleteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteHealthInsurance

Description:Deletes a health insurance record for a user.
🔸 Request Payload (deleteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	insuranceId
	Int32
	✅
	Insurance ID to delete
	🔸 Response Fields (deleteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteMedicationAndAllergies

Description:Deletes a medication and allergies record for a user.
🔸 Request Payload (deleteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	recordId
	Int32
	✅
	Record ID to delete
	🔸 Response Fields (deleteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________




API: SubmitAhdForm

Description:Submits an Advance Health Directive form for a user.
🔸 Request Payload (SubmitFormRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID submitting the form
	formId
	Int32
	✅
	Form ID
	responses
	ResponseDetail[]
	✅
	List of question responses
	isFinalSubmission
	Bool
	 
	Is this the final submission
	

Nested Type: ResponseDetail
Field
	Type
	Required
	Description
	questionId
	Int32
	✅
	Question ID
	answer
	String
	✅
	Answer to the question
	🔸 Response Fields (SubmitFormResponse)
 
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if submission succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	 


________________


API: UpdateNotes

Description:Updates a note for a user.
🔸 Request Payload (UpdateNotesRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the note
	noteId
	Int32
	✅
	Note ID to update
	note
	String
	✅
	Updated note content
	🔸 Response Fields (CreateNoteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateFamilyDoctor

Description:Updates family doctor details for a user.
🔸 Request Payload (UpdateFamilyDoctorRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the record
	doctorId
	Int32
	✅
	Doctor ID to update
	doctorName
	String
	✅
	Updated doctor name
	contact
	String
	 
	Updated contact details
	🔸 Response Fields (UpdateFamilyDoctorResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateMedicationAndAllergies

Description:Updates medication and allergies details for a user.
🔸 Request Payload (UpdateMedicationAndAllergiesRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the record
	recordId
	Int32
	✅
	Record ID to update
	medication
	String
	 
	Updated medication name
	allergy
	String
	 
	Updated allergy details
	🔸 Response Fields (UpdateMedicationAndAllergiesResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteNote

Description:Deletes a note for a user.
🔸 Request Payload (DeleteNoteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	noteId
	Int32
	✅
	Note ID to delete
	🔸 Response Fields (DeleteNoteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateHealthInsurance

Description:Updates health insurance details for a user.
🔸 Request Payload (UpdateHealthInsuranceRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the record
	insuranceId
	Int32
	✅
	Insurance ID to update
	insuranceName
	String
	 
	Updated insurance name
	policyNumber
	String
	 
	Updated policy number
	provider
	String
	 
	Updated insurance provider
	🔸 Response Fields (CreateHealthInsuranceResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateAllergy

Description:Creates a new allergy record for a user.
🔸 Request Payload (CreateAllergyRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the record
	allergy
	String
	✅
	Allergy details
	🔸 Response Fields (CreateAllergyResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteAllergyDetails

Description:Deletes an allergy record for a user.
🔸 Request Payload (deleteRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	allergyId
	Int32
	✅
	Allergy ID to delete
	🔸 Response Fields (deleteResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateAllergies

Description:Updates allergy details for a user.
🔸 Request Payload (UpdateAllergyRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the record
	allergyId
	Int32
	✅
	Allergy ID to update
	allergy
	String
	 
	Updated allergy details
	🔸 Response Fields (UpdateAllergyResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CreateMeicalHistoryV2

Description:Creates a new medical history record (version 2) for a user.
🔸 Request Payload (CreateMedicalHistoryV2Request)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID creating the record
	history
	String
	✅
	Medical history details
	🔸 Response Fields (MedicalHistoryResponseV2)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if creation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateMedicalHistory

Description:Updates medical history details for a user.
🔸 Request Payload (UpdateMedicalHistoryRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the record
	historyId
	Int32
	✅
	Medical history ID to update
	history
	String
	 
	Updated medical history
	🔸 Response Fields (UpdateMedicalHistoryResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________




API: AddQuestionsToSection

Description:Adds questions to a section.
🔸 Request Payload (AddQuestionsToSectionRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID adding the questions
	sectionId
	Int32
	✅
	Section ID to add questions
	stateId
	Int32
	✅
	State ID
	countryId
	Int32
	✅
	Country ID
	questions
	SectionQuestionInput[]
	✅
	List of questions
	Nested Type: SectionQuestionInput
Field
	Type
	Required
	Description
	questionHeader
	String
	✅
	Question header
	questionDescription
	String
	 
	Question description
	questionType
	String
	✅
	Question type
	questionOptions
	String[]
	 
	List of options
	

🔸 Response Fields (AddQuestionsToSectionResponse)
 
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	 


________________


API: UpdateQuestionsToSection

Description:Updates questions in a section.
🔸 Request Payload (UpdateQuestionsToSectionRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the questions
	ahdQuestionId
	Int32
	✅
	AHD Question ID to update
	sectionId
	Int32
	✅
	Section ID to update
	stateId
	Int32
	✅
	State ID
	countryId
	Int32
	✅
	Country ID
	questions
	SectionQuestionInput[]
	✅
	List of updated questions
	Nested Type: SectionQuestionInput
Field
	Type
	Required
	Description
	questionHeader
	String
	✅
	Question header
	questionDescription
	String
	 
	Question description
	questionType
	String
	✅
	Question type
	questionOptions
	String[]
	 
	List of options
	🔸 Response Fields (UpdateQuestionsToSectionResponse)
 
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	 


________________


API: DeleteQuestionFromSection

Description:Deletes a question from a section.
🔸 Request Payload (DeleteQuestionFromSectionRequest)
Field
	Type
	Required
	Description
	sectionId
	Int32
	✅
	Section ID
	questionId
	Int32
	✅
	Question ID to delete
	🔸 Response Fields (DeleteQuestionFromSectionResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________




API: SubmitAhdFormV2

Description:Submits an Advance Health Directive form (version 2) for a user.
🔸 Request Payload (SubmitAHDFormRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID submitting the form
	id
	Int32
	✅
	Personal details ID
	responses
	Response[]
	✅
	List of question responses
	Nested Type: Response
Field
	Type
	Required
	Description
	questionId
	Int32
	✅
	Question ID
	sectionId
	Int32
	✅
	Section ID
	responseValue
	String[]
	✅
	Response value(s)
	contactId
	Int32
	 
	Contact ID
	relatedTo
	Int32
	 
	Related to ID
	agentTypeId
	Int32
	 
	Agent type ID
	keys
	String
	 
	Key for special handling
	subResponses
	SubResponse[]
	 
	List of sub-responses
	Nested Type: SubResponse
Field
	Type
	Required
	Description
	subQuestionId
	Int32
	✅
	Sub-question ID
	subResponseValue
	String
	✅
	Sub-response value
	contactId
	Int32
	 
	Contact ID
	🔸 Response Fields (SubmitAHDFormResponse)
 
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if submission succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	 


________________


API: DeleteAHDForm

Description:Deletes an Advance Health Directive form for a user.
🔸 Request Payload (DeleteAHDRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	id
	Int32
	✅
	Personal details ID to delete
	🔸 Response Fields (DeleteAHDResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: SetAHDPersonalDetails

Description:Sets or updates personal details for Advance Health Directive.
🔸 Request Payload (SetPersonalDetailsRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	stateId
	Int32
	✅
	State ID
	countryId
	Int32
	✅
	Country ID
	declarationDate
	String
	 
	Declaration date
	fullName
	String
	✅
	Full name
	streetNameAndNumber
	String
	 
	Street name and number
	city
	String
	 
	City
	apartmentNumber
	String
	 
	Apartment number
	pincode
	String
	 
	Pincode
	signedAhdBefore
	Bool
	 
	Signed AHD before
	institutionName
	String
	 
	Institution name
	selectedSections
	String
	 
	Selected sections
	updatedBy
	String
	 
	User ID who updated
	🔸 Response Fields (SetPersonalDetailsResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if operation succeeded
	message
	String
	 
	Informational message
	errorMessage
	String
	 
	Error message if failed
	________________




API: SubmitAhdFormV3

Description:Submits an Advance Health Directive form (version 3) for a user, including witness and QR code generation.
🔸 Request Payload (SubmitAHDFormRequestV3)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID submitting the form
	id
	Int32
	✅
	Personal details ID
	stateId
	Int32
	✅
	State ID
	countryId
	Int32
	✅
	Country ID
	declarationDate
	String
	 
	Declaration date
	fullName
	String
	✅
	Full name
	streetNameAndNumber
	String
	 
	Street name and number
	city
	String
	 
	City
	apartmentNumber
	String
	 
	Apartment number
	pincode
	String
	 
	Pincode
	signedAhdBefore
	Bool
	 
	Signed AHD before
	institutionName
	String
	 
	Institution name
	selectedSections
	String
	 
	Selected sections
	completionStatus
	String
	 
	Completion status
	responses
	Response[]
	✅
	List of question responses
	Nested Type: Response
Field
	Type
	Required
	Description
	questionId
	Int32
	✅
	Question ID
	sectionId
	Int32
	✅
	Section ID
	responseValue
	String
	✅
	Response value
	contactId
	Int32
	 
	Contact ID
	relatedTo
	Int32
	 
	Related to ID
	agentTypeId
	Int32
	 
	Agent type ID
	keys
	String
	 
	Key for special handling
	subResponses
	SubResponse[]
	 
	List of sub-responses
	Nested Type: SubResponse
Field
	Type
	Required
	Description
	subQuestionId
	Int32
	✅
	Sub-question ID
	subResponseValue
	String
	✅
	Sub-response value
	contactId
	Int32
	 
	Contact ID
	🔸 Response Fields (SubmitAHDFormResponseV3)
Field
	Type
	Required
	Description
	ahdUserId
	Int32
	✅
	ID of the AHD user personal details
	qrLink
	String
	 
	Link embedded in the QR code
	qrCode
	String
	 
	Base64-encoded QR code image
	success
	Bool
	✅
	Indicates if submission succeeded
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if failed
	recordIdentifier
	String
	 
	Unique record identifier
	id
	Int32
	 
	Personal details ID
	________________


API: AddAhdContacts

Description:Adds new AHD contacts for a user.
🔸 Request Payload (AddAhdContactsRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID adding the contact
	contacts
	Contact[]
	✅
	List of contact details
	Nested Type: Contact
Field
	Type
	Required
	Description
	contactId
	Int32
	 
	Contact ID
	name
	String
	✅
	Contact name
	phone
	String
	 
	Phone number
	email
	String
	 
	Email address
	relation
	String
	 
	Relation to user
	🔸 Response Fields (AddAhdContactsResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateAhdContacts

Description:Updates AHD contact details for a user.
🔸 Request Payload (UpdateAhdContactsRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID updating the contact
	contactId
	Int32
	✅
	Contact ID to update
	contact
	Contact
	✅
	Updated contact details
	Nested Type: Contact
Field
	Type
	Required
	Description
	contactId
	Int32
	 
	Contact ID
	name
	String
	✅
	Contact name
	phone
	String
	 
	Phone number
	email
	String
	 
	Email address
	relation
	String
	 
	Relation to user
	🔸 Response Fields (UpdateAhdContactsResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: ListAllAhdContacts

Description:Lists all AHD contacts for a user.
🔸 Request Payload (ListAllAhdContactsRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to list contacts
	🔸 Response Fields (ListAllAhdContactsResponse)
Field
	Type
	Required
	Description
	contacts
	Contact[]
	✅
	List of contact details
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if operation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	Nested Type: Contact
Field
	Type
	Required
	Description
	contactId
	Int32
	 
	Contact ID
	name
	String
	✅
	Contact name
	phone
	String
	 
	Phone number
	email
	String
	 
	Email address
	relation
	String
	 
	Relation to user
	________________


API: DeleteAhdContact

Description:Deletes an AHD contact for a user.
🔸 Request Payload (DeleteAhdContactRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID performing the delete
	contactId
	Int32
	✅
	Contact ID to delete
	🔸 Response Fields (DeleteAhdContactResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: WitnessSignUp

Description:Registers a witness for an AHD form.
🔸 Request Payload (WitnessSignUpRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID registering witness
	witness
	Witness
	✅
	Witness details
	Nested Type: Witness
Field
	Type
	Required
	Description
	witnessId
	Int32
	 
	Witness ID
	name
	String
	✅
	Witness name
	phone
	String
	 
	Phone number
	email
	String
	 
	Email address
	🔸 Response Fields (WitnessSignUpResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if signup succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: WitnessConsent

Description:Records consent from a witness for an AHD form.
🔸 Request Payload (WitnessConsentRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	witnessId
	Int32
	✅
	Witness ID
	consent
	Bool
	✅
	Consent status
	🔸 Response Fields (WitnessConsentResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if consent recorded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: ResetAHDForm

Description:Resets an AHD form for a user.
🔸 Request Payload (ResetAHDRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID resetting the form
	id
	Int32
	✅
	Personal details ID
	🔸 Response Fields (ResetAHDResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if reset succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: SeverityDropDown

Description:Fetches severity dropdown options.
🔸 Request Payload (GetSeverityRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	🔸 Response Fields (GetSeverityResponse)
Field
	Type
	Required
	Description
	severities
	Severity[]
	✅
	List of severity options
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if fetch succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	Nested Type: Severity
Field
	Type
	Required
	Description
	severityId
	Int32
	✅
	Severity ID
	name
	String
	✅
	Severity name
	________________


API: AddAgentWitness

Description:Adds an agent witness for a user.
🔸 Request Payload (AddAgentWitnessRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID adding witness
	witness
	Witness
	✅
	Witness details
	Nested Type: Witness
Field
	Type
	Required
	Description
	witnessId
	Int32
	 
	Witness ID
	name
	String
	✅
	Witness name
	phone
	String
	 
	Phone number
	email
	String
	 
	Email address
	🔸 Response Fields (AddAgentWitnessResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: MedicalAgentSignUp

Description:Registers a medical agent for a user.
🔸 Request Payload (AgentSignUpRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID registering agent
	agent
	Agent
	✅
	Agent details
	Nested Type: Agent
Field
	Type
	Required
	Description
	agentId
	Int32
	 
	Agent ID
	name
	String
	✅
	Agent name
	phone
	String
	 
	Phone number
	email
	String
	 
	Email address
	🔸 Response Fields (AgentSignUpResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if signup succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: CombinedLogin

Description:Performs a combined login for user and agent.
🔸 Request Payload (CombinedLoginRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	agentId
	String
	✅
	Agent ID
	password
	String
	✅
	Password
	🔸 Response Fields (CombinedLoginResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if login succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: VerifyAhdPasscode

Description:Verifies the AHD passcode for a user.
🔸 Request Payload (VerifyAhdPasscodeRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	passcode
	String
	✅
	Passcode to verify
	🔸 Response Fields (VerifyAhdPasscodeResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if verification succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteHealthFiles

Description:Deletes health files for a user.
🔸 Request Payload (DeleteFilesHD)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	fileIds
	Int32[]
	✅
	List of file IDs to delete
	🔸 Response Fields (DeleteFilesHDResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: HealthFileReupload

Description:Reuploads a health file for a user.
🔸 Request Payload (HealthFileReuploadRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	fileId
	Int32
	✅
	File ID to reupload
	fileData
	String
	✅
	File data (base64)
	🔸 Response Fields (HealthFileReuploadResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if reupload succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: PrintPdfHealth

Description:Generates and returns a PDF of health data for a user.
🔸 Request Payload (PrintPdfHealthRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	vaultId
	Int32
	 
	Vault ID
	moduleIds
	Int32[]
	 
	List of module IDs
	moduleNames
	String[]
	 
	List of module names
	🔸 Response Fields (PrintPdfHealthResponse)
Field
	Type
	Required
	Description
	message
	String
	 
	Informational message
	success
	Bool
	✅
	Indicates if PDF generated
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if failed
	doctor
	Doctor[]
	 
	List of doctor details
	medicalhistory
	MedicalHistory
	 
	Medical history details
	data
	Medication[]
	 
	Medication data
	health_insurances
	HealthInsurance[]
	 
	Health insurance details
	notes
	Note[]
	 
	Notes
	questionsFromSection
	QuestionsFromSection[]
	 
	Questions from section
	ahdUserPersonalDetails
	AhdUserPersonalDetails
	 
	AHD user personal details
	allergies
	AllergyForUser[]
	 
	Allergies for user
	supplements
	Supplement[]
	 
	Supplements
	medicalPOA
	GetMymedicalPoaResponseData[]
	 
	Medical POA data
	familyMedicalResponses
	QuestionResponses[]
	 
	Family medical responses
	emergencyFamilyMedicalResponses
	QuestionResponses[]
	 
	Emergency family medical responses
	wholeFamilyMedicalResponses
	MedicalUserResponse
	 
	Whole family medical responses
	healthCareAccountIds
	HealthAccountInfo[]
	 
	Health care account IDs
	medicalHistoryForm
	UserResponse
	 
	Medical history form
	vaultName
	String
	 
	Vault name
	



Nested Type: Doctor
Field
	Type
	Required
	Description
	doctorId
	Int32
	     ✅
	Doctor ID
	name
	String
	     ✅
	Doctor name
	specialty
	String
	 
	Specialty
	contact
	String
	 
	Contact details
	________________


Nested Type: MedicalHistory
Field
	Type
	Required
	Description
	historyId
	Int32
	     ✅
	Medical history ID
	condition
	String
	     ✅
	Condition name
	description
	String
	 
	Condition description
	diagnosedDate
	String
	 
	Date diagnosed
	status
	String
	 
	Current status
	________________


Nested Type: Medication
Field
	Type
	Required
	Description
	medicationId
	Int32
	     ✅
	Medication ID
	name
	String
	     ✅
	Medication name
	dosage
	String
	 
	Dosage information
	frequency
	String
	 
	Frequency of intake
	notes
	String
	 
	Additional notes
	________________


Nested Type: HealthInsurance
Field
	Type
	Required
	Description
	insuranceId
	Int32
	     ✅
	Insurance ID
	provider
	String
	     ✅
	Insurance provider
	policyNumber
	String
	     ✅
	Policy number
	coverage
	String
	 
	Coverage details
	________________


Nested Type: Note
Field
	Type
	Required
	Description
	noteId
	Int32
	     ✅
	Note ID
	content
	String
	     ✅
	Note content
	createdAt
	String
	 
	Creation timestamp
	________________


Nested Type: QuestionsFromSection
Field
	Type
	Required
	Description
	questionId
	Int32
	      ✅
	Question ID
	sectionId
	Int32
	      ✅
	Section ID
	questionText
	String
	      ✅
	Question text
	options
	String[]
	 
	List of options
	answer
	String
	 
	User's answer
	________________


Nested Type: AhdUserPersonalDetails
Field
	Type
	Required
	Description
	id
	Int32
	     ✅
	Personal details ID
	fullName
	String
	     ✅
	Full name
	address
	String
	 
	Address
	city
	String
	 
	City
	stateId
	Int32
	 
	State ID
	countryId
	Int32
	 
	Country ID
	declarationDate
	String
	 
	Declaration date
	________________


Nested Type: AllergyForUser
Field
	Type
	Required
	Description
	allergyId
	Int32
	     ✅
	Allergy ID
	name
	String
	     ✅
	Allergy name
	severity
	String
	 
	Severity
	notes
	String
	 
	Additional notes
	________________


Nested Type: Supplement
Field
	Type
	Required
	Description
	supplementId
	Int32
	     ✅
	Supplement ID
	name
	String
	     ✅
	Supplement name
	dosage
	String
	 
	Dosage information
	frequency
	String
	 
	Frequency of intake
	________________


Nested Type: GetMymedicalPoaResponseData
Field
	Type
	Required
	Description
	poaId
	Int32
	    ✅
	POA ID
	agentName
	String
	    ✅
	Agent name
	relation
	String
	 
	Relation to user
	contact
	String
	 
	Contact details
	________________


Nested Type: QuestionResponses
Field
	Type
	Required
	Description
	questionId
	Int32
	     ✅
	Question ID
	response
	String
	     ✅
	User's response
	sectionId
	Int32
	 
	Section ID
	________________


Nested Type: MedicalUserResponse
Field
	Type
	Required
	Description
	userId
	String
	     ✅
	User ID
	responses
	QuestionResponses[]
	 
	List of responses
	summary
	String
	 
	Summary of responses
	________________


Nested Type: HealthAccountInfo
Field
	Type
	Required
	Description
	accountId
	Int32
	     ✅
	Account ID
	accountName
	String
	     ✅
	Account name
	provider
	String
	 
	Provider name
	________________


Nested Type: UserResponse
Field
	Type
	Required
	Description
	userId
	String
	     ✅
	User ID
	responses
	QuestionResponses[]
	 
	List of responses
	formId
	Int32
	 
	Form ID
	



________________


API: AddHealthCareAccount

Description:Adds a health care account for a user.
🔸 Request Payload (HealthCareAccountReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	account
	HealthAccountInfo
	✅
	Account details
	Nested Type: HealthAccountInfo
Field
	Type
	Required
	Description
	accountId
	Int32
	✅
	Account ID
	accountName
	String
	✅
	Account name
	provider
	String
	 
	Provider name
	🔸 Response Fields (HealthCareResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateHealthCareAccount

Description:Updates health care account details for a user.
🔸 Request Payload (HealthCareAccountReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	accountId
	Int32
	✅
	Account ID to update
	account
	HealthAccountInfo
	✅
	Updated account details
	Nested Type: HealthAccountInfo
Field
	Type
	Required
	Description
	accountId
	Int32
	✅
	Account ID
	accountName
	String
	✅
	Account name
	provider
	String
	 
	Provider name
	🔸 Response Fields (HealthCareResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: DeleteHealthCareAccount

Description:Deletes a health care account for a user.
🔸 Request Payload (deleteHealthCareAccReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	accountId
	Int32
	✅
	Account ID to delete
	🔸 Response Fields (deleteHealthCareAccRes)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: AddSupplement

Description:Adds a supplement for a user.
🔸 Request Payload (AddSupplementReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	supplement
	Supplement
	✅
	Supplement details
	Nested Type: Supplement
Field
	Type
	Required
	Description
	supplementId
	Int32
	✅
	Supplement ID
	name
	String
	✅
	Supplement name
	dosage
	String
	 
	Dosage information
	frequency
	String
	 
	Frequency of intake
	🔸 Response Fields (AddSupplementResp)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________






API: UpdateSupplement

Description:Updates a supplement and its associated files for a user.
🔸 Request Payload (UpdateSupplementReq)
Field
	Type
	Required
	Description
	supplementId
	Int32
	✅
	Supplement ID to update
	userId
	String
	✅
	User ID
	supplementName
	String
	 
	Updated supplement name
	dosage
	String
	 
	Updated dosage
	notes
	String
	 
	Updated notes
	important
	Bool
	 
	Mark as important
	files
	SupplementFile[]
	 
	List of associated files
	updatedBy
	String
	 
	User ID who updated
	Nested Type: SupplementFile
Field
	Type
	Required
	Description
	fileid
	Int32
	✅
	File ID
	documentLink
	String
	✅
	Document link (base64/file)
	originalFilename
	String
	 
	Original file name
	createdBy
	String
	 
	Creator's user ID
	updatedBy
	String
	 
	Updater's user ID
	createdAt
	String
	 
	Creation timestamp
	updatedAt
	String
	 
	Update timestamp
	🔸 Response Fields (UpdateSupplementResp)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	id
	Int32
	 
	Supplement ID
	recordIdentifier
	String
	 
	Unique record identifier
	________________


API: DeleteSupplement

Description:Deletes a supplement for a user.
🔸 Request Payload (DeleteSupplementReq)
Field
	Type
	Required
	Description
	supplementId
	Int32
	✅
	Supplement ID to delete
	userId
	String
	✅
	User ID
	🔸 Response Fields (DeleteSupplementResp)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if delete succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: ServeHealthVaultFile

Description:Serves a health vault file for a user.
🔸 Request Payload (ServeHealthFileReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	fileId
	Int32
	✅
	File ID to serve
	🔸 Response Fields (ServeHealthFileRes)
Field
	Type
	Required
	Description
	fileData
	String
	✅
	File data (base64)
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if operation succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: AddMymedicalRecord

Description:Adds a medical record for a user.
🔸 Request Payload (MymedicalRecordReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	record
	String
	✅
	Medical record details
	🔸 Response Fields (MymedicalRecordRes)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if addition succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: UpdateMymedicalRecord

Description:Updates a medical record for a user.
🔸 Request Payload (MymedicalRecordReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	recordId
	Int32
	✅
	Record ID to update
	record
	String
	✅
	Updated medical record
	🔸 Response Fields (MymedicalRecordRes)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: updateMedicalAgeBloodGroup

Description:Updates age and blood group for a user.
🔸 Request Payload (AgeBloodGroup)
Field
	Type
	Required
	Description
	age
	Int32
	✅
	Age
	bloodGroup
	Int32
	✅
	Blood group ID
	userId
	String
	✅
	User ID
	🔸 Response Fields (UpdateCountryResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: EmergencyAlert

Description:Fetches age and blood group for emergency alert.
🔸 Request Payload (GetAgeBloodGroupSingleReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	type
	Int32
	✅
	Type
	🔸 Response Fields (GetAgeBloodGroupSingleRes)
Field
	Type
	Required
	Description
	age
	Int32
	 
	Age
	bloodGroupId
	Int32
	 
	Blood group ID
	bloodGroup
	String
	 
	Blood group name
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if fetch succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: updateEmergencyAlert

Description:Updates emergency alert details for a user.
🔸 Request Payload (emergencyAlertReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	alert
	String
	✅
	Alert details
	🔸 Response Fields (UpdateCountryResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if update succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: BraceletAhd

Description:Fetches AHD details for bracelet integration.
🔸 Request Payload (GetAllHealthVaultFilesReq)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	🔸 Response Fields (GetAhdRes)
Field
	Type
	Required
	Description
	data
	GetAhdDataRes[]
	✅
	List of AHD data
	Nested Type: GetAhdDataRes
Field
	Type
	Required
	Description
	ahdId
	Int32
	✅
	AHD ID
	question_header
	String
	✅
	Question header
	________________


API: SubmitConsentConfirmationHealth

Description:Submits consent confirmation for health POA.
🔸 Request Payload (HealthConsentConfrimationRequest)
Field
	Type
	Required
	Description
	id
	String
	✅
	Agent ID
	isAccept
	Bool
	✅
	Consent status
	🔸 Response Fields (HealthConsentConfrimationResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	error
	String
	 
	Error message if failed
	________________


API: ResendPersonaOtpHealth
Description:Resends OTP for persona verification.
🔸 Request Payload (resendOtpRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	personaId
	String
	✅
	Persona ID
	🔸 Response Fields (resendOtpResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if resend succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: RevokeByRole

Description:Revokes access by role for a user.
🔸 Request Payload (RevokeByRoleRequest)
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	role
	String
	✅
	Role to revoke
	🔸 Response Fields (RevokeByRoleResponse)
Field
	Type
	Required
	Description
	code
	Int32
	 
	Status code
	success
	Bool
	✅
	Indicates if revoke succeeded
	message
	String
	 
	Informational message
	error
	String
	 
	Error message if failed
	________________


API: RejectHealthModuleAccess

Description:Rejects access to a health module.
🔸 Request Payload (RemoveAccess)
Field
	Type
	Required
	Description
	personaId
	String
	✅
	Persona ID
	modules
	String
	✅
	Modules to reject
	flag
	Bool
	✅
	Flag for rejection
	🔸 Response Fields (rejectMouduleAccessResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if failed
	success
	Bool
	✅
	Indicates if rejection succeeded
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	sharedMoudules
	String[]
	 
	List of shared modules
	sharedVaults
	String
	 
	Shared vaults
	recipientUserId
	String
	 
	Recipient user ID
	senderName
	String
	 
	Sender name
	________________


API: rejectHealthPoaModuleAccess

Description:Rejects access to a health POA module.
🔸 Request Payload (RemoveAccess)
Field
	Type
	Required
	Description
	personaId
	String
	✅
	Persona ID
	modules
	String
	✅
	Modules to reject
	flag
	Bool
	✅
	Flag for rejection
	🔸 Response Fields (rejectMouduleAccessResponse)
Field
	Type
	Required
	Description
	errorMessage
	String
	 
	Error message if failed
	success
	Bool
	✅
	Indicates if rejection succeeded
	message
	String
	 
	Informational message
	code
	Int32
	 
	Status code
	sharedMoudules
	String[]
	 
	List of shared modules
	sharedVaults
	String
	 
	Shared vaults
	recipientUserId
	String
	 
	Recipient user ID
	senderName
	String
	 
	Sender name
	________________















Digital Vault Service API Documentation




API LIST :
API: GetSocialMediaRecords


Description: Fetches a list of social media records for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	The ID of the user whose social media records are fetched.
	page
	Int32
	✅
	The page number for pagination.
	count
	Int32
	✅
	The number of records per page.
	🔸 Response Fields (data array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the social media record.
	userId
	String
	✅
	ID of the user associated with the record.
	files
	FileRecord[]
	

	List of files associated with the record.
	serviceAccountNickname
	String
	✅
	Nickname of the social media account.
	usrnameOrEmailid
	String
	✅
	Username or email ID for the account.
	password
	String
	✅
	Password for the account.
	recoveryEmail
	String
	

	Recovery email for the account.
	recoveryCode
	String
	

	Recovery code for the account.
	twoFactorAuthType
	String
	

	Type of two-factor authentication.
	amount
	Float
	

	Payment amount for the account.
	frequency
	String
	

	Payment frequency (e.g., monthly, yearly).
	paymentMode
	String
	

	Payment mode (e.g., credit card, UPI).
	renewalDate
	String
	

	Renewal date for the account.
	notes
	String
	

	Additional notes for the account.
	legacyNote
	String
	

	Legacy note for the account.
	familyNote
	String
	

	Family note for the account.
	accStatusAfterPassingId
	Int32
	✅
	Account status after passing ID.
	serviceId
	Int32
	✅
	Service ID for the social media platform.
	selectedContactsId
	Int32[]
	

	List of contact IDs associated with the account.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedAt
	String
	✅
	Timestamp of the last update.
	serviceName
	String
	✅
	Name of the social media service.
	accStatusAfterPassingName
	String
	✅
	Name of the account status after passing.
	openbaoKeyName
	String
	✅
	Openbao key name for the record.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	othersTypeName
	String
	

	Custom type name for the account.
	________________


Nested Type: FileRecord


Field
	Type
	Required
	Description
	fileUrl
	String
	✅
	The URL of the file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file.
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who updated the file.
	id
	Int32
	✅
	The unique identifier for the file.
	



API: CreateOrUpdateSocialMediaEntry
Description: Creates or updates a social media entry for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int32
	

	Unique identifier for updating an existing record.
	userId
	String
	✅
	ID of the user associated with the record.
	files
	FileUpload[]
	

	List of files to upload with the record.
	serviceAccountNickname
	String
	✅
	Nickname of the social media account.
	usrnameOrEmailid
	String
	✅
	Username or email ID for the account.
	password
	String
	✅
	Password for the account.
	recoveryEmail
	String
	

	Recovery email for the account.
	recoveryCode
	String
	

	Recovery code for the account.
	twoFactorAuthType
	String
	

	Type of two-factor tools.
	amount
	Float
	

	Payment amount for the account.
	frequency
	String
	

	Payment frequency (e.g., monthly, yearly).
	paymentMode
	String
	

	Payment mode (e.g., credit card, UPI).
	renewalDate
	String
	

	Renewal date for the account.
	notes
	String
	

	Additional notes for the account.
	legacyNote
	String
	

	Legacy note for the account.
	familyNote
	String
	

	Family note for the account.
	accStatusAfterPassingId
	Int32
	✅
	Account status after passing ID.
	serviceId
	Int32
	✅
	Service ID for the social media platform.
	selectedContactsId
	Int32[]
	

	List of contact IDs associated with the account.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	createdAt
	String
	

	Timestamp of when the record was created.
	updatedAt
	String
	

	Timestamp of the last update.
	othersTypeName
	String
	

	Custom type name for the account.
	🔸 Response Fields
Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	data.id
	Int32
	✅
	Unique identifier for the created/updated record.
	data.emailFiles
	FileRecord[]
	

	List of files associated with the record.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type: FileUpload


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file upload.
	file
	Bytes
	✅
	The binary content of the file being uploaded.
	originalFilename
	String
	✅
	The original name of the file being uploaded.
	createdBy
	String
	✅
	The identifier of the user who initiated the file upload.
	updatedBy
	String
	✅
	The identifier of the user who last updated the file upload.
	action
	String
	✅
	The action associated with the file upload (e.g., create, update).
	Nested Type: FileRecord




Field
	Type
	Required
	Description
	fileUrl
	String
	✅
	The URL of the file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file.
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who updated the file.
	id
	Int32
	✅
	The unique identifier for the file.
	



API: DeleteSocialMediaRecord
Description: Deletes a social media record for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier of the social media record to delete.
	userId
	String
	✅
	ID of the user associated with the record.
	updatedBy
	String
	✅
	ID of the user who is deleting the entry.
	🔸 Response Fields
Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	________________


API: GetSocialMediaRecordById
Description: Fetches a specific social media record by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the record.
	recordId
	Int32
	✅
	Unique identifier of the social media record.
	🔸 Response Fields
Field
	Type
	Required
	Description
	data.id
	Int32
	✅
	Unique identifier for the social media record.
	data.userId
	String
	✅
	ID of the user associated with the record.
	data.files
	FileRecord[]
	

	List of files associated with the record.
	data.serviceAccountNickname
	String
	✅
	Nickname of the social media account.
	data.usrnameOrEmailid
	String
	✅
	Username or email ID for the account.
	data.password
	String
	✅
	Password for the account.
	data.recoveryEmail
	String
	

	Recovery email for the account.
	data.recoveryCode
	String
	

	Recovery code for the account.
	data.twoFactorAuthType
	String
	

	Type of two-factor authentication.
	data.amount
	Float
	

	Payment amount for the account.
	data.frequency
	String
	

	Payment frequency (e.g., monthly, yearly).
	data.paymentMode
	String
	

	Payment mode (e.g., credit card, UPI).
	data.renewalDate
	String
	

	Renewal date for the account.
	data.notes
	String
	

	Additional notes for the account.
	data.legacyNote
	String
	

	Legacy note for the account.
	data.familyNote
	String
	

	Family note for the account.
	data.accStatusAfterPassingId
	Int32
	✅
	Account status after passing ID.
	data.serviceId
	Int32
	✅
	Service ID for the social media platform.
	data.selectedContactsId
	Int32[]
	

	List of contact IDs associated with the account.
	data.createdBy
	String
	✅
	ID of the user who created the entry.
	data.updatedBy
	String
	✅
	ID of the user who last updated the entry.
	data.createdAt
	String
	✅
	Timestamp of when the record was created.
	data.updatedAt
	String
	✅
	Timestamp of the last update.
	data.serviceName
	String
	✅
	Name of the social media service.
	data.accStatusAfterPassingName
	String
	✅
	Name of the account status after passing.
	data.openbaoKeyName
	String
	✅
	Openbao key name for the record.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	data.othersTypeName
	String
	

	Custom type name for the account.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	error
	String
	

	Error message if the request fails.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	________________


Nested Type: FileRecord




Field
	Type
	Required
	Description
	fileUrl
	String
	✅
	The URL of the file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file.
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who updated the file.
	id
	Int32
	✅
	The unique identifier for the file.
	

API: getPrivateFolderTypes
Description: Fetches all private folder types.
🔸 Request Payload
Field
	Type
	Required
	Description
	None
	-
	-
	No request payload required.
	🔸 Response Fields
Field
	Type
	Required
	Description
	folderTypes.id
	Int32
	✅
	Unique identifier for the folder type.
	folderTypes.folderType
	String
	✅
	Name of the folder type.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	



API: createPrivateFolder
Description: Creates a new private folder for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	note
	String
	

	Additional notes for the private folder.
	familyNote
	String
	

	Family note for the private folder.
	privateFolderType
	Int32
	✅
	Type ID of the private folder.
	otherFolderType
	String
	

	Custom folder type name, if applicable.
	accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	selectedContactIds
	Int32[]
	

	List of contact IDs associated with the folder.
	userId
	String
	✅
	ID of the user creating the folder.
	files
	File[]
	

	List of files to be uploaded with the folder.
	createdBy
	String
	✅
	ID of the user who created the folder.
	🔸 Response Fields
Field
	Type
	Required
	Description
	error
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	data.files
	PrivateFolderFiles[]
	

	List of files associated with the folder.
	data.id
	Int32
	✅
	Unique identifier for the created folder.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type:File  


Field
	Type
	Required
	Description
	file
	Bytes
	✅
	The binary content of the file.
	originalFileName
	String
	✅
	The original name of the file.
	id
	Int32
	✅
	The unique identifier for the file.
	action
	String
	✅
	The action associated with the file (e.g., create, update, delete).


	Nested Type:PrivateFolderFiles


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file in the private folder.
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault.
	file_type
	String
	✅
	The type or format of the file (e.g., PDF, image).
	originalFilename
	String
	✅
	The original name of the file.
	created_at
	String
	✅
	The timestamp when the file was created.
	created_by
	String
	✅
	The identifier of the user who created the file.
	updated_at
	String
	✅
	The timestamp when the file was last updated.
	updated_by
	String
	✅
	The identifier of the user who last updated the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	

API: getPrivateFolderByUserId
Description: Fetches all private folders for a user with pagination.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user whose private folders are fetched.
	page
	Int32
	✅
	The page number for pagination.
	limit
	Int32
	✅
	The number of records per page.
	🔸 Response Fields (data array)        
Field
	Type
	Required
	Description
	note
	String
	

	Additional notes for the private folder.
	familyNote
	String
	

	Family note for the private folder.
	privateFolderType
	Int32
	✅
	Type ID of the private folder.
	privateFolderTypeName
	String
	✅
	Name of the private folder type.
	otherFolderType
	String
	

	Custom folder type name, if applicable.
	accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	selectedContactIds
	Int32[]
	

	List of contact IDs associated with the folder.
	created_at
	String
	✅
	Timestamp of when the folder was created.
	created_by
	String
	✅
	ID of the user who created the folder.
	updated_at
	String
	✅
	Timestamp of the last update.
	updated_by
	String
	✅
	ID of the user who last updated the folder.
	totalFilesUploaded
	Int32
	✅
	Total number of files uploaded to the folder.
	files
	PrivateFolderFiles[]
	

	List of files associated with the folder.
	id
	Int32
	✅
	Unique identifier for the folder.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	________________


Nested Type:PrivateFolderFiles


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file in the private folder.
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault.
	file_type
	String
	✅
	The type or format of the file (e.g., PDF, image).
	originalFilename
	String
	✅
	The original name of the file.
	created_at
	String
	✅
	The timestamp when the file was created.
	created_by
	String
	✅
	The identifier of the user who created the file.
	updated_at
	String
	✅
	The timestamp when the file was last updated.
	updated_by
	String
	✅
	The identifier of the user who last updated the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	

API: deletePrivateFolder
Description: Deletes a private folder for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the folder.
	privateFolderId
	Int32
	✅
	Unique identifier of the private folder to delete.
	deletedBy
	String
	✅
	ID of the user who is deleting the folder.
	🔸 Response Fields
Field
	Type
	Required
	Description
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	________________


API: updatePrivateFolder
Description: Updates an existing private folder for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	privateFolderId
	Int32
	✅
	Unique identifier of the folder to update.
	userId
	String
	✅
	ID of the user associated with the folder.
	updatedBy
	String
	✅
	ID of the user who is updating the folder.
	note
	String
	

	Updated notes for the private folder.
	familyNote
	String
	

	Updated family note for the private folder.
	privateFolderType
	Int32
	✅
	Updated type ID of the private folder.
	otherFolderType
	String
	

	Updated custom folder type name, if applicable.
	accStatusAfterPassing
	Int32
	✅
	Updated status of the account after passing.
	selectedContactIds
	Int32[]
	

	Updated list of contact IDs associated with the folder.
	files
	File[]
	

	Updated list of files to be uploaded with the folder.
	createdBy
	String
	✅
	ID of the user who created the folder.
	🔸 Response Fields
Field
	Type
	Required
	Description
	error
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	data.files
	PrivateFolderFiles[]
	

	List of files associated with the updated folder.
	data.id
	Int32
	✅
	Unique identifier for the updated folder.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type:File  


Field
	Type
	Required
	Description
	file
	Bytes
	✅
	The binary content of the file.
	originalFileName
	String
	✅
	The original name of the file.
	id
	Int32
	✅
	The unique identifier for the file.
	action
	String
	✅
	The action associated with the file (e.g., create, update, delete).


	Nested Type:PrivateFolderFiles


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file in the private folder.
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault.
	file_type
	String
	✅
	The type or format of the file (e.g., PDF, image).
	originalFilename
	String
	✅
	The original name of the file.
	created_at
	String
	✅
	The timestamp when the file was created.
	created_by
	String
	✅
	The identifier of the user who created the file.
	updated_at
	String
	✅
	The timestamp when the file was last updated.
	updated_by
	String
	✅
	The identifier of the user who last updated the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	

API: getPrivateFolderById
Description: Fetches a specific private folder by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the folder.
	privateFolderId
	Int32
	✅
	Unique identifier of the private folder.
	🔸 Response Fields
Field
	Type
	Required
	Description
	data.note
	String
	

	Additional notes for the private folder.
	data.familyNote
	String
	

	Family note for the private folder.
	data.privateFolderType
	Int32
	✅
	Type ID of the private folder.
	data.privateFolderTypeName
	String
	✅
	Name of the private folder type.
	data.otherFolderType
	String
	

	Custom folder type name, if applicable.
	data.accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	data.selectedContactIds
	Int32[]
	

	List of contact IDs associated with the folder.
	data.created_at
	String
	✅
	Timestamp of when the folder was created.
	data.created_by
	String
	✅
	ID of the user who created the folder.
	data.updated_at
	String
	✅
	Timestamp of the last update.
	data.updated_by
	String
	✅
	ID of the user who last updated the folder.
	data.totalFilesUploaded
	Int32
	✅
	Total number of files uploaded to the folder.
	data.files
	PrivateFolderFiles[]
	

	List of files associated with the folder.
	data.id
	Int32
	✅
	Unique identifier for the folder.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	Nested Type:PrivateFolderFiles


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file in the private folder.
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault.
	file_type
	String
	✅
	The type or format of the file (e.g., PDF, image).
	originalFilename
	String
	✅
	The original name of the file.
	created_at
	String
	✅
	The timestamp when the file was created.
	created_by
	String
	✅
	The identifier of the user who created the file.
	updated_at
	String
	✅
	The timestamp when the file was last updated.
	updated_by
	String
	✅
	The identifier of the user who last updated the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	

API: GetManageDevicesRecords
Description: Fetches a list of device records for a user with pagination.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	The ID of the user whose device records are fetched.
	page
	Int32
	✅
	The page number for pagination.
	count
	Int32
	✅
	The number of records per page.
	🔸 Response Fields (data array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the device record.
	userId
	String
	✅
	ID of the user associated with the device.
	files
	FileRecord[]
	

	List of files associated with the device.
	deviceType
	String
	✅
	Type of the device (e.g., laptop, phone).
	deviceName
	String
	✅
	Name of the device.
	accessTypeID
	Int32
	✅
	ID of the access type for the device.
	accessTypeName
	String
	✅
	Name of the access type.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedAt
	String
	✅
	Timestamp of the last update.
	page
	Int32
	✅
	Current page number.
	count
	Int32
	✅
	Number of records returned in the response.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	error
	String
	

	Error message if the request fails.
	message
	String
	✅
	Response message.
	________________


Nested Type: FileRecord


Field
	Type
	Required
	Description
	fileUrl
	String
	✅
	The URL of the file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file.
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who updated the file.
	id
	Int32
	✅
	The unique identifier for the file.
	

API: CreateOrUpdateManageDevices
Description: Creates or updates a device record for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int32
	

	Unique identifier for updating an existing device record.
	userId
	String
	✅
	ID of the user associated with the device.
	files
	FileUpload[]
	

	List of files to upload with the device record.
	deviceType
	String
	✅
	Type of the device (e.g., laptop, phone).
	deviceName
	String
	✅
	Name of the device.
	accessTypeID
	Int32
	✅
	ID of the access type for the device.
	accessTypeName
	String
	✅
	Name of the access type.
	notes
	String
	

	Additional notes for the device.
	createdBy
	String
	✅
	ID of the user who created the entry.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	🔸 Response Fields
Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	data.id
	Int32
	✅
	Unique identifier for the created/updated device record.
	data.files
	FileRecord[]
	

	List of files associated with the device.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type: FileUpload


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file upload.
	file
	Bytes
	✅
	The binary content of the file being uploaded.
	originalFilename
	String
	✅
	The original name of the file being uploaded.
	createdBy
	String
	✅
	The identifier of the user who initiated the file upload.
	updatedBy
	String
	✅
	The identifier of the user who last updated the file upload.
	action
	String
	✅
	The action associated with the file upload (e.g., create, update).
	Nested Type: FileRecord


Field
	Type
	Required
	Description
	fileUrl
	String
	✅
	The URL of the file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file.
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who updated the file.
	id
	Int32
	✅
	The unique identifier for the file.
	

API: DeleteManageDevicesRecordbyID
Description: Deletes a specific device record by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the device record.
	id
	Int32
	✅
	Unique identifier of the device record to delete.
	🔸 Response Fields
Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	________________


API: GetManageDevicesByUserId
Description: Fetches all device records for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user whose device records are fetched.
	🔸 Response Fields (data array)
Field
	Type
	Required
	Description
	date
	String
	✅
	Date associated with the device record.
	deviceType
	String
	✅
	Type of the device (e.g., laptop, phone).
	deviceName
	String
	✅
	Name of the device.
	accessTypeId
	Int32
	✅
	ID of the access type for the device.
	accesssTypeName
	String
	✅
	Name of the access type.
	accessTypeValue
	String
	✅
	Value of the access type.
	id
	Int32
	✅
	Unique identifier for the device record.
	userId
	String
	✅
	ID of the user associated with the device.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	createdBy
	String
	✅
	ID of the user who created the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetManageDevicesById
Description: Fetches a specific device record by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier of the device record.
	userId
	String
	✅
	ID of the user associated with the device record.
	🔸 Response Fields
Field
	Type
	Required
	Description
	data.date
	String
	✅
	Date associated with the device record.
	data.deviceType
	String
	✅
	Type of the device (e.g., laptop, phone).
	data.deviceName
	String
	✅
	Name of the device.
	data.accessTypeId
	Int32
	

	ID of the access type for the device.
	data.accesssTypeName
	String
	✅
	Name of the access type.
	data.accessTypeValue
	String
	✅
	Value of the access type.
	data.notes
	String
	

	Additional notes for the device.
	data.id
	Int32
	

	Unique identifier for the device record.
	data.userId
	String
	✅
	ID of the user associated with the device.
	data.files
	manageFiles[]
	

	List of files associated with the device.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	Nested Type: manageFiles


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the file.
	manageDevicesId
	Int32
	✅
	The identifier of the associated device record.
	FileURL
	String
	✅
	The URL of the file.
	fileType
	String
	✅
	The type or format of the file (e.g., PDF, image).
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who last updated the file.
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was last updated.
	OriginalFileName
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	

API: DeleteManageDevices
Description: Deletes all device records for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	The ID of the user whose device records are to be deleted.
	🔸 Response Fields
Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	________________


API: GetAccessTypes
Description: Fetches all access types for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	The ID of the user whose access types are fetched.
	🔸 Response Fields (accessTypes array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the access type.
	name
	String
	✅
	Name of the access type.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetEmailPurpose
Description: Fetches all email purposes.
🔸 Request Payload
Field
	Type
	Required
	Description
	none
	-
	-
	No request payload required.
	🔸 Response Fields (emailPurpose array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the email purpose.
	purpose
	String
	✅
	Name of the email purpose.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetEmailAccounts
Description: Fetches a list of email accounts for a user with pagination.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	The ID of the user whose email accounts are fetched.
	page
	Int32
	✅
	The page number for pagination.
	limit
	Int32
	✅
	The number of records per page.
	🔸 Response Fields (emailAccountList array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the email account.
	userId
	String
	✅
	ID of the user associated with the account.
	emailNickName
	String
	✅
	Nickname for the email account.
	emailId
	String
	✅
	Email address of the account.
	password
	String
	✅
	Password for the email account.
	isEmailPrimary
	Boolean
	✅
	Indicates if this is the primary email.
	useForCommunication
	Boolean
	✅
	Indicates if this email is preferred for communication.
	recoveryEmail
	String
	

	Recovery email address for the account.
	recoveryCode
	String
	

	Recovery code for the account.
	twoFactorIsOn
	Boolean
	✅
	Indicates if two-factor authentication is enabled.
	twoFactorAuthType
	String
	

	Type of two-factor authentication (e.g., SMS, App).
	likedWithSubscriptions
	Boolean
	✅
	Indicates if the email is linked to a subscription.
	legacyNote
	String
	

	Legacy note for the account.
	familyNote
	String
	

	Family note for the account.
	accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	emailIdType
	Int32
	✅
	Type ID of the email account.
	selectedContactID
	Int32
	

	ID of the selected contact associated with the account.
	Date
	String
	

	Date associated with the account.
	emailType
	String
	

	Type of the email account.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	createdBy
	String
	✅
	ID of the user who created the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	PrimaryEmail
	String
	

	Primary email address, if applicable.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	totalPages
	Int32
	✅
	Total number of pages in the paginated response.
	totalRecords
	Int32
	✅
	Total number of records available.
	currentPage
	Int32
	✅
	Current page number in the paginated response.
	________________


API: AddEmailAccount
Description: Creates a new email account entry for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	accountNickName
	String
	✅
	Nickname for the email account.
	emailPurpuse
	Int32
	✅
	Purpose ID of the email account.
	emailId
	String
	✅
	Email address of the account.
	password
	String
	✅
	Password for the email account.
	isPrimaryMail
	Boolean
	✅
	Indicates if this is the primary email.
	isPreferredForCommunication
	Boolean
	✅
	Indicates if this email is preferred for communication.
	recoveryEmail
	String
	

	Recovery email address for the account.
	recoveryCode
	String
	

	Recovery code for the account.
	isTwoFactorEnabled
	Boolean
	✅
	Indicates if two-factor authentication is enabled.
	authType
	String
	

	Type of authentication used (e.g., SMS, App).
	isMailLinkedToSubscription
	Boolean
	✅
	Indicates if the email is linked to a subscription.
	shouldAgentDeleteAccount
	Boolean
	✅
	Indicates if the agent should delete the account.
	shouldTransferToFamily
	Boolean
	✅
	Indicates if the account should be transferred to family.
	contacts
	Int32[]
	

	List of contact IDs associated with the account.
	familyNote
	String
	

	Family note for the account.
	userId
	String
	✅
	ID of the user creating the account.
	primaryMailId
	String
	

	ID of the primary email, if applicable.
	legacyNote
	String
	

	Legacy note for the account.
	accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	emailFiles
	EmailFileRequest[]
	

	List of files to be uploaded with the account.
	otherEmailPurpose
	String
	

	Custom purpose for the email, if applicable.
	createdBy
	String
	✅
	ID of the user who created the entry.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	data.accountNickName
	String
	✅
	Nickname for the email account.
	data.emailPurpuse
	Int32
	✅
	Purpose ID of the email account.
	data.email
	String
	✅
	Email address of the account.
	data.password
	String
	✅
	Password for the email account.
	data.isPrimaryMail
	Boolean
	✅
	Indicates if this is the primary email.
	data.isPreferredForCommunication
	Boolean
	✅
	Indicates if this email is preferred for communication.
	data.recoveryEmail
	String
	

	Recovery email address for the account.
	data.recoveryCode
	String
	

	Recovery code for the account.
	data.isTwoFactorEnabled
	Boolean
	✅
	Indicates if two-factor authentication is enabled.
	data.authType
	String
	

	Type of authentication used.
	data.isMailLinkedToSubscription
	Boolean
	✅
	Indicates if the email is linked to a subscription.
	data.shouldAgentDeleteAccount
	Boolean
	✅
	Indicates if the agent should delete the account.
	data.shouldTransferToFamily
	Boolean
	✅
	Indicates if the account should be transferred to family.
	data.contacts
	Int32[]
	

	List of contact IDs associated with the account.
	data.familyNote
	String
	

	Family note for the account.
	data.userId
	String
	✅
	ID of the user associated with the account.
	data.primaryMailId
	String
	

	ID of the primary email, if applicable.
	data.legacyNote
	String
	

	Legacy note for the account.
	data.accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	data.emailFiles
	fileList[]
	

	List of files associated with the account.
	data.otherEmailPurpose
	String
	

	Custom purpose for the email, if applicable.
	data.createdBy
	String
	✅
	ID of the user who created the entry.
	data.id
	Int32
	✅
	Unique identifier for the created account.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	


Nested Type: EmailFileRequest



Field
	Type
	Required
	Description
	file
	Bytes
	✅
	The binary content of the file being uploaded for the email account.
	originalFilename
	String
	✅
	The original name of the file being uploaded.
	



API: UpdateEmailAccount
Description: Updates an existing email account entry for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	accountNickName
	String
	✅
	Nickname for the email account.
	emailPurpuse
	Int32
	✅
	Purpose ID of the email account.
	email
	String
	✅
	Email address of the account.
	password
	String
	✅
	Password for the email account.
	isPrimaryMail
	Boolean
	✅
	Indicates if this is the primary email.
	isPreferredForCommunication
	Boolean
	✅
	Indicates if this email is preferred for communication.
	recoveryEmail
	String
	

	Recovery email address for the account.
	recoveryCode
	String
	

	Recovery code for the account.
	isTwoFactorEnabled
	Boolean
	✅
	Indicates if two-factor authentication is enabled.
	authType
	String
	

	Type of authentication used (e.g., SMS, App).
	isMailLinkedToSubscription
	Boolean
	✅
	Indicates if the email is linked to a subscription.
	shouldAgentDeleteAccount
	Boolean
	✅
	Indicates if the agent should delete the account.
	shouldTransferToFamily
	Boolean
	✅
	Indicates if the account should be transferred to family.
	contacts
	Int32[]
	

	List of contact IDs associated with the account.
	familyNote
	String
	

	Family note for the account.
	userId
	String
	✅
	ID of the user associated with the account.
	primaryMailId
	String
	

	ID of the primary email, if applicable.
	legacyNote
	String
	

	Legacy note for the account.
	accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	emailFiles
	updateEmailFileRequest[]
	

	List of files to be updated for the account.
	Id
	Int32
	✅
	Unique identifier of the email account to update.
	createdBy
	String
	✅
	ID of the user who created the entry.
	OtherEmailPurpose
	String
	

	Custom purpose for the email, if applicable.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	data.id
	Int32
	✅
	Unique identifier for the updated account.
	data.emailFiles
	fileList[]
	

	List of files associated with the account.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type: EmailFileRequest


Field
	Type
	Required
	Description
	file
	Bytes
	✅
	The binary content of the file being updated for the email account.
	originalFilename
	String
	✅
	The original name of the file being updated.
	
Nested Type: fileList


Field
	Type
	Required
	Description
	originalName
	String
	✅
	The original name of the file.
	documentLink
	String
	✅
	The link or URL to access the file.
	id
	Int64
	✅
	The unique identifier for the file.
	created_at
	String
	✅
	The timestamp when the file was created.
	

API: DeleteEmailAccount
Description: Deletes a specific email account by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the email account.
	id
	Int64
	✅
	Unique identifier of the email account to delete.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetEmailAccountById
Description: Fetches a specific email account by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the email account.
	id
	Int32
	✅
	Unique identifier of the email account.
	🔸 Response Fields
Field
	Type
	Required
	Description
	message
	String
	✅
	Response message.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	error
	String
	

	Error message if the request fails.
	emailAccount.id
	Int32
	✅
	Unique identifier for the email account.
	emailAccount.userId
	String
	✅
	ID of the user associated with the account.
	emailAccount.emailNickName
	String
	✅
	Nickname for the email account.
	emailAccount.emailId
	String
	✅
	Email address of the account.
	emailAccount.password
	String
	✅
	Password for the email account.
	emailAccount.primaryEmail
	String
	

	Primary email address, if applicable.
	emailAccount.isEmailPrimary
	Boolean
	✅
	Indicates if this is the primary email.
	emailAccount.useForCommunication
	Boolean
	✅
	Indicates if this email is preferred for communication.
	emailAccount.recoveryEmail
	String
	

	Recovery email address for the account.
	emailAccount.recoveryCode
	String
	

	Recovery code for the account.
	emailAccount.twoFactorIsOn
	Boolean
	✅
	Indicates if two-factor authentication is enabled.
	emailAccount.twoFactorAuthType
	String
	

	Type of two-factor authentication (e.g., SMS, App).
	emailAccount.likedWithSubscriptions
	Boolean
	✅
	Indicates if the email is linked to a subscription.
	emailAccount.legacyNote
	String
	

	Legacy note for the account.
	emailAccount.familyNote
	String
	

	Family note for the account.
	emailAccount.accStatusAfterPassing
	Int32
	✅
	Status of the account after passing.
	emailAccount.emailIdType
	Int32
	✅
	Type ID of the email account.
	emailAccount.selectedContactID
	Int32
	

	ID of the selected contact associated with the account.
	emailAccount.Date
	String
	

	Date associated with the account.
	emailAccount.emailType
	String
	

	Type of the email account.
	emailAccount.otherPurpose
	String
	

	Custom purpose for the email, if applicable.
	emailAccount.contacts
	Int32[]
	

	List of contact IDs associated with the account.
	emailAccount.choice
	String
	

	Choice associated with the account, if applicable.
	emailAccount.files
	fileList[]
	

	List of files associated with the account.
	emailAccount.updated_at
	String
	

	Timestamp of the last update.
	emailAccount.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type: fileList


Field
	Type
	Required
	Description
	originalName
	String
	✅
	The original name of the file.
	documentLink
	String
	✅
	The link or URL to access the file.
	id
	Int64
	✅
	The unique identifier for the file.
	created_at
	String
	✅
	The timestamp when the file was created.
	

API: GetSocialMediaServiceTypes
Description: Fetches all social media service types.
🔸 Request Payload
Field
	Type
	Required
	Description
	none
	-
	-
	No request payload required.
	🔸 Response Fields (data array)
Field
	Type
	Required
	Description
	name
	String
	✅
	Name of the social media service type.
	id
	Int32
	✅
	Unique identifier for the service type.
	message
	String
	✅
	Response message.
	success
	Boolean
	✅
	Indicates success or failure of the request.
	error
	String
	

	Error message if the request fails.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	________________


API: DeleteEmailFile
Description: Deletes a specific file associated with an email account.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the email account.
	fileID
	Int32
	✅
	Unique identifier of the file to delete.
	emailAccountId
	Int32
	✅
	Unique identifier of the email account.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	



API: GetSubscriptionType
Description: Fetches all subscription types.
🔸 Request Payload
Field
	Type
	Required
	Description
	none
	-
	-
	No request payload required.
	🔸 Response Fields (GetSubscriptionTypes array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the subscription type.
	name
	String
	✅
	Name of the subscription type.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetServiceNames
Description: Fetches all service names.
🔸 Request Payload
Field
	Type
	Required
	Description
	none
	-
	-
	No request payload required.
	🔸 Response Fields (GetServiceNames array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the service name.
	name
	String
	✅
	Name of the service.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetSubscriptions
Description: Fetches a list of subscriptions for a user with pagination.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user whose subscriptions are fetched.
	page
	Int32
	✅
	The page number for pagination.
	limit
	Int32
	✅
	The number of records per page.
	🔸 Response Fields (allSubscriptions array)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the subscription.
	openbaoKeyName
	String
	✅
	Key name associated with the subscription.
	usernameEmail
	String
	✅
	Username or email associated with the subscription.
	recoveryEmail
	String
	

	Recovery email for the subscription.
	recoveryCode
	String
	

	Recovery code for the subscription.
	authType
	String
	

	Authentication type (e.g., SMS, App).
	amount
	Double
	✅
	Payment amount for the subscription.
	frequency
	String
	✅
	Payment frequency (e.g., monthly, yearly).
	paymentMode
	String
	✅
	Payment mode (e.g., credit card, UPI).
	renewalDate
	String
	

	Renewal date (null if auto-renewal is off).
	accStatusAfterPassingId
	Int32
	✅
	Status of the account after passing.
	subServiceNames
	String
	✅
	Name of the subscription service.
	subscriptionsTypes
	String
	✅
	Type of the subscription.
	legacyNote
	String
	

	Legacy note for the subscription.
	familyNote
	String
	

	Family note for the subscription.
	selectedContactsId
	Int32
	✅
	ID of the selected contact associated with the subscription.
	password
	String
	✅
	Password for the subscription.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	createdBy
	String
	✅
	ID of the user who created the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	totalPages
	Int32
	✅
	Total number of pages in the paginated response.
	totalRecords
	Int32
	✅
	Total number of records available.
	currentPage
	Int32
	✅
	Current page number in the paginated response.
	________________


API: GetSubscriptionByID
Description: Fetches a specific subscription by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the subscription.
	Id
	Int32
	✅
	Unique identifier of the subscription.
	🔸 Response Fields (Subscription)
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the subscription.
	usernameEmail
	String
	✅
	Username or email associated with the subscription.
	recoveryEmail
	String
	

	Recovery email for the subscription.
	recoveryCode
	String
	

	Recovery code for the subscription.
	authType
	String
	

	Authentication type (e.g., SMS, App).
	amount
	Double
	✅
	Payment amount for the subscription.
	frequency
	String
	✅
	Payment frequency (e.g., monthly, yearly).
	paymentMode
	String
	✅
	Payment mode (e.g., credit card, UPI).
	renewalDate
	String
	

	Renewal date (null if auto-renewal is off).
	accStatusAfterPassingId
	Int32
	✅
	Status of the account after passing.
	subServiceNamesID
	Int32
	✅
	ID of the subscription service name.
	subscriptionsTypesID
	Int32
	✅
	ID of the subscription type.
	legacyNote
	String
	

	Legacy note for the subscription.
	familyNote
	String
	

	Family note for the subscription.
	selectedContactsId
	Int32[]
	

	List of contact IDs associated with the subscription.
	TwoFactorIsOn
	Boolean
	✅
	Indicates if two-factor authentication is enabled.
	PaymentsDetailIsOn
	Boolean
	✅
	Indicates if payment details are included.
	AutoRenewal
	Boolean
	✅
	Indicates if auto-renewal is enabled.
	AgentManage
	Boolean
	✅
	Indicates if the subscription is managed by an agent.
	password
	String
	✅
	Password for the subscription.
	AllFile
	FileSub[]
	

	List of files associated with the subscription.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	subscriptionTypeName
	String
	✅
	Name of the subscription type.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


Nested Type: FileSub


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the subscription file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was last updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who last updated the file.
	DocumentLink
	String
	✅
	The link or URL to access the file.
	

API: UpdateSubscription
Description: Updates an existing subscription for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int32
	✅
	Unique identifier for the subscription to update.
	userId
	String
	✅
	ID of the user associated with the subscription.
	usernameEmail
	String
	✅
	Username or email associated with the subscription.
	recoveryEmail
	String
	

	Recovery email for the subscription.
	recoveryCode
	String
	

	Recovery code for the subscription.
	authType
	String
	

	Authentication type (e.g., SMS, App).
	amount
	Double
	✅
	Payment amount for the subscription.
	frequency
	String
	✅
	Payment frequency (e.g., monthly, yearly).
	paymentMode
	String
	✅
	Payment mode (e.g., credit card, UPI).
	renewalDate
	String
	

	Renewal date (null if auto-renewal is off).
	accStatusAfterPassingId
	Int32
	✅
	Status of the account after passing.
	subServiceNamesID
	Int32
	✅
	ID of the subscription service name.
	subscriptionsTypesID
	Int32
	✅
	ID of the subscription type.
	legacyNote
	String
	

	Legacy note for the subscription.
	familyNote
	String
	

	Family note for the subscription.
	selectedContactsId
	Int32[]
	

	List of contact IDs associated with the subscription.
	SubscriptionFiles
	UpdateSubscriptionFile[]
	

	List of files to be updated for the subscription.
	OpenbaoKeyName
	String
	✅
	Key name associated with the subscription.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	password
	String
	✅
	Password for the subscription.
	subscriberTypeName
	String
	✅
	Name of the subscriber type.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	data.id
	Int32
	✅
	Unique identifier for the updated subscription.
	data.files
	FileSub[]
	

	List of files associated with the subscription.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	



Nested Type: UpdateSubscriptionFile



Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the subscription file being updated.
	file
	Bytes
	✅
	The binary content of the file being updated.
	originalFilename
	String
	✅
	The original name of the file being updated.
	Action
	String
	✅
	The action associated with the file update (e.g., update, replace).
	

API: CreateSubscription
Description: Creates a new subscription for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the subscription.
	usernameEmail
	String
	✅
	Username or email associated with the subscription.
	recoveryEmail
	String
	

	Recovery email for the subscription.
	recoveryCode
	String
	

	Recovery code for the subscription.
	authType
	String
	

	Authentication type (e.g., SMS, App).
	amount
	Double
	✅
	Payment amount for the subscription.
	frequency
	String
	✅
	Payment frequency (e.g., monthly, yearly).
	paymentMode
	String
	✅
	Payment mode (e.g., credit card, UPI).
	renewalDate
	String
	

	Renewal date (null if auto-renewal is off).
	accStatusAfterPassingId
	Int32
	✅
	Status of the account after passing.
	subServiceNamesID
	Int32
	✅
	ID of the subscription service name.
	subscriptionsTypesID
	Int32
	✅
	ID of the subscription type.
	legacyNote
	String
	

	Legacy note for the subscription.
	familyNote
	String
	

	Family note for the subscription.
	selectedContactsId
	Int32[]
	

	List of contact IDs associated with the subscription.
	OpenbaoKeyName
	String
	✅
	Key name associated with the subscription.
	SubscriptionFiles
	CreateSubscriptionFileRequest[]
	

	List of files to be uploaded for the subscription.
	createdBy
	String
	✅
	ID of the user who created the entry.
	password
	String
	✅
	Password for the subscription.
	subscriptionTypeName
	String
	✅
	Name of the subscription type.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	data.id
	Int32
	✅
	Unique identifier for the created subscription.
	data.SubscriptionFiles
	FileSub[]
	

	List of files associated with the subscription.
	data.recordIdentifier
	String
	✅
	Unique UUID for traceability.
	________________


Nested Type: CreateSubscriptionFileRequest


Field
	Type
	Required
	Description
	file
	Bytes
	✅
	The binary content of the file being uploaded for the subscription.
	originalFilename
	String
	✅
	The original name of the file being uploaded.
	Action
	String
	✅
	The action associated with the file creation (e.g., create).
	Nested Type: FileSub


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the subscription file.
	originalFilename
	String
	✅
	The original name of the file.
	fileContent
	String
	✅
	The content of the file (likely a reference or encoded data).
	createdAt
	String
	✅
	The timestamp when the file was created.
	updatedAt
	String
	✅
	The timestamp when the file was last updated.
	createdBy
	String
	✅
	The identifier of the user who created the file.
	updatedBy
	String
	✅
	The identifier of the user who last updated the file.
	DocumentLink
	String
	✅
	The link or URL to access the file.
	

API: DeleteSubscription
Description: Deletes a specific subscription by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the subscription.
	Id
	Int32
	✅
	Unique identifier of the subscription to delete.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: DeleteFilesDm
Description: Deletes a specific file associated with a digital vault module.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the file.
	id
	Int32
	✅
	Unique identifier of the file to delete.
	type
	String
	✅
	Type of the digital vault module (e.g., email, subscription).
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: DigitalFileReupload
Description: Reuploads a file to a specific digital vault module.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the file.
	id
	Int32
	✅
	Unique identifier of the file to reupload.
	type
	String
	✅
	Type of the digital vault module (e.g., email, subscription).
	fileContent
	Bytes
	✅
	Content of the file to be reuploaded.
	fileName
	String
	✅
	Name of the file.
	actualId
	Int32
	✅
	Actual identifier of the record associated with the file.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	fileName
	String
	✅
	Name of the reuploaded file.
	fileContent
	String
	✅
	Content or reference to the reuploaded file.
	________________


API: GetDigitalDashboardProgress
Description: Fetches the progress of digital vault modules for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user whose progress is fetched.
	vaults
	VaultAndGroupsInDigital[]
	✅
	List of vaults and their associated groups and modules.
	🔸 Response Fields (data array)
Field
	Type
	Required
	Description
	vaultId
	Int32
	✅
	Unique identifier for the vault.
	vaultName
	String
	✅
	Name of the vault.
	groups
	GroupsInDigital[]
	✅
	List of groups within the vault.
	groups.groupId
	Int32
	✅
	Unique identifier for the group.
	groups.groupName
	String
	✅
	Name of the group.
	groups.modules
	ModulesInGroupDigital[]
	✅
	List of modules within the group.
	groups.modules.subModuleId
	Int32
	✅
	Unique identifier for the submodule.
	groups.modules.moduleName
	String
	✅
	Name of the module.
	groups.modules.completed
	Float
	✅
	Percentage of completion for the module.
	groups.modules.Remaining
	Float
	✅
	Percentage remaining for the module.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	

Nested Type: GroupsInDigital


Field
	Type
	Required
	Description
	groupId
	Int32
	✅
	The unique identifier for the group within the digital vault.
	groupName
	String
	✅
	The name of the group.
	modules
	repeated ModulesInGroupDigital
	✅
	A list of modules associated with the group.
	Nested Type: ModulesInGroupDigital


Field
	Type
	Required
	Description
	subModuleId
	Int32
	✅
	The unique identifier for the submodule within the group
	moduleName
	String
	✅
	The name of the module
	completed
	Float
	✅
	The completion percentage or status of the module
	Remaining
	Float
	✅
	The remaining percentage or status of the module
	

API: PrintPdfDigital
Description: Generates a PDF report for digital vault data based on specified modules.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user requesting the PDF.
	vaultId
	Int32
	✅
	Unique identifier of the vault.
	moduleIds
	Int32[]
	✅
	List of module IDs to include in the PDF.
	moduleNames
	String[]
	✅
	List of module names corresponding to the module IDs.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	allSubscriptionSub
	SubscriptionSub[]
	

	List of subscription records.
	allEmailDetails
	EmailDetails[]
	

	List of email account details.
	allSocialMediaRecord
	SocialMediaRecord[]
	

	List of social media records.
	allManageDevicesRecord
	manageDevicesMetaData[]
	

	List of managed device records.
	allPrivateFolderData
	PrivateFolderData[]
	

	List of private folder data.
	AllOtherAccDetails
	OtherAccDetails[]
	

	List of other account details.
	vaultName
	String
	✅
	Name of the vault.
	________________


Nested Type: OtherAccDetails


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the other account record
	openbao_key_name
	string
	✅
	Key name used for encryption or vault access
	account_type
	string
	✅
	Type of the account (e.g., Gaming, Streaming, Membership)
	platform_name
	string
	✅
	Name of the platform or service provider
	username
	string
	✅
	Username associated with the account
	password
	string
	✅
	Password for accessing the account
	recovery_email
	string
	✅
	Recovery email linked to the account
	recovery_code
	string
	✅
	Backup code or recovery key for the account
	auth_type
	string
	✅
	Type of authentication (e.g., SMS, App-based 2FA)
	family_note
	string
	✅
	Note for family members about this account
	legacy_note
	string
	✅
	Instructions or notes for legacy access to the account
	acc_status_after_passing_id
	int32
	✅
	ID representing the desired account status after passing
	selected_contacts_id
	int32
	✅
	ID referencing selected contacts who may access this account
	created_by
	string
	✅
	Identifier of the user who created this account record
	created_at
	string
	✅
	Timestamp when the account record was created
	updated_by
	string
	✅
	Identifier of the user who last updated the record
	updated_at
	string
	✅
	Timestamp when the record was last updated
	

Nested Type : PrivateFolderData


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the private folder
	openbao_key_name
	string
	✅
	Key name used for secure vault encryption or access
	folder_name
	string
	✅
	Name of the private folder
	folder_description
	string
	✅
	Description or purpose of the folder
	folder_password
	string
	✅
	Password required to access the folder
	recovery_email
	string
	✅
	Recovery email associated with the folder
	recovery_code
	string
	✅
	Recovery code for accessing the folder
	family_note
	string
	✅
	Note for family members regarding the folder
	legacy_note
	string
	✅
	Note regarding legacy instructions for the folder
	created_by
	string
	✅
	Identifier of the user who created the folder
	created_at
	string
	✅
	Timestamp when the folder was created
	updated_by
	string
	✅
	Identifier of the user who last updated the folder
	updated_at
	string
	✅
	Timestamp when the folder was last updated
	

Nested Type : manageDevicesMetaData


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the device metadata entry
	openbao_key_name
	string
	✅
	Key name used for encryption or secure vault access
	device_type
	string
	✅
	Type of device (e.g., Laptop, Mobile, Tablet)
	brand
	string
	✅
	Brand or manufacturer of the device
	model
	string
	✅
	Model name or number of the device
	os
	string
	✅
	Operating system running on the device (e.g., Windows, iOS)
	serial_number
	string
	✅
	Serial number uniquely identifying the device
	device_password
	string
	✅
	Password or PIN for unlocking the device
	recovery_email
	string
	✅
	Recovery email associated with the device, if any
	recovery_code
	string
	✅
	Recovery code or backup key for the device
	family_note
	string
	✅
	Note for family members about this device
	legacy_note
	string
	✅
	Note about legacy instructions for the device
	created_by
	string
	✅
	Identifier of the user who created this metadata
	created_at
	string
	✅
	Timestamp when this metadata was created
	updated_by
	string
	✅
	Identifier of the user who last updated this metadata
	updated_at
	string
	✅
	Timestamp when this metadata was last updated
	



Nested Type: SubscriptionSub



Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the subscription
	openbaoKeyName
	String
	✅
	The key name used for encryption or access in the vault
	usernameEmail
	String
	✅
	The username or email associated with the subscription
	recoveryEmail
	String
	✅
	The recovery email for the subscription account
	recoveryCode
	String
	✅
	The recovery code for the subscription account
	authType
	String
	✅
	The authentication type (e.g., SMS, App)
	amount
	Double
	✅
	The payment amount for the subscription
	frequency
	String
	✅
	The payment frequency (e.g., monthly, yearly)
	paymentMode
	String
	✅
	The payment mode (e.g., credit card, UPI)
	renewalDate
	String
	✅
	The renewal date for the subscription (null if auto-renewal is off)
	accStatusAfterPassingId
	Int32
	✅
	The ID representing the account status after the user's passing
	subServiceNames
	String
	✅
	The name of the subscription service
	subscriptionsTypes
	String
	✅
	The type of subscription
	legacyNote
	String
	✅
	A note regarding legacy instructions for the subscription
	familyNote
	String
	✅
	A note for family members regarding the subscription
	selectedContactsId
	Int32
	✅
	The ID of selected contacts associated with the subscription
	password
	String
	✅
	The password for the subscription account
	recordIdentifier
	String
	✅
	A unique identifier for the subscription record
	createdBy
	String
	✅
	The identifier of the user who created the subscription
	createdAt
	String
	✅
	The timestamp when the subscription was created
	updatedBy
	String
	✅
	The identifier of the user who last updated the subscription
	updatedAt
	String
	✅
	The timestamp when the subscription was last updated
	

Nested Type: EmailDetails




Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the email account
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault
	email
	String
	✅
	The email address associated with the account
	password
	String
	✅
	The password for the email account
	recovery_email
	String
	✅
	The recovery email for the account
	recovery_code
	String
	✅
	The recovery code for the account
	auth_type
	String
	✅
	The authentication type (e.g., SMS, App)
	family_note
	String
	✅
	A note for family members regarding the email account
	legacy_note
	String
	✅
	A note regarding legacy instructions for the account
	acc_status_after_passing_id
	Int32
	✅
	The ID representing the account status after the user's passing
	selected_contacts_id
	Int32
	✅
	The ID of selected contacts associated with the account
	created_by
	String
	✅
	The identifier of the user who created the email account record
	created_at
	String
	✅
	The timestamp when the email account record was created
	updated_by
	String
	✅
	The identifier of the user who last updated the email account record
	updated_at
	String
	✅
	The timestamp when the email account record was last updated
	

Nested Type : SocialMediaRecord




Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the social media account
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault
	platform
	String
	✅
	The social media platform (e.g., Facebook, Twitter)
	username
	String
	✅
	The username associated with the social media account
	password
	String
	✅
	The password for the social media account
	recovery_email
	String
	✅
	The recovery email for the account
	recovery_code
	String
	✅
	The recovery code for the account
	auth_type
	String
	✅
	The authentication type (e.g., SMS, App)
	family_note
	String
	✅
	A note for family members regarding the account
	legacy_note
	String
	✅
	A note regarding legacy instructions for the account
	acc_status_after_passing_id
	Int32
	✅
	The ID representing the account status after the user's passing
	selected_contacts_id
	Int32
	✅
	The ID of selected contacts associated with the account
	created_by
	String
	✅
	The identifier of the user who created the account record
	created_at
	String
	✅
	The timestamp when the account record was created
	updated_by
	String
	✅
	The identifier of the user who last updated the account record
	updated_at
	String
	✅
	The timestamp when the account record was last updated
	

API: KeyMasterPrintPdf
Description: Generates a PDF report for key master data based on specified modules.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user requesting the PDF.
	vaultId
	Int32
	✅
	Unique identifier of the vault.
	moduleIds
	Int32[]
	✅
	List of module IDs to include in the PDF.
	moduleNames
	String[]
	✅
	List of module names corresponding to the module IDs.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	allManageDevicesRecord
	manageDevicesMetaData[]
	

	List of managed device records.
	allSocialMediaRecord
	SocialMediaRecord[]
	

	List of social media records.
	allSubscriptionSub
	SubscriptionSub[]
	

	List of subscription records.
	AllOtherAccDetails
	OtherAccDetails[]
	

	List of other account details.
	allEmailDetails
	EmailDetails[]
	

	List of email account details.
	________________





Nested Type: SocialMediaRecord


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the social media account
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault
	platform
	String
	✅
	The social media platform (e.g., Facebook, Twitter)
	username
	String
	✅
	The username associated with the social media account
	password
	String
	✅
	The password for the social media account
	recovery_email
	String
	✅
	The recovery email for the account
	recovery_code
	String
	✅
	The recovery code for the account
	auth_type
	String
	✅
	The authentication type (e.g., SMS, App)
	family_note
	String
	✅
	A note for family members regarding the account
	legacy_note
	String
	✅
	A note regarding legacy instructions for the account
	acc_status_after_passing_id
	Int32
	✅
	The ID representing the account status after the user's passing
	selected_contacts_id
	Int32
	✅
	The ID of selected contacts associated with the account
	created_by
	String
	✅
	The identifier of the user who created the account record
	created_at
	String
	✅
	The timestamp when the account record was created
	updated_by
	String
	✅
	The identifier of the user who last updated the account record
	updated_at
	String
	✅
	The timestamp when the account record was last updated
	Nested Type : manageDevicesMetaData
Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the device metadata entry
	openbao_key_name
	string
	✅
	Key name used for encryption or secure vault access
	device_type
	string
	✅
	Type of device (e.g., Laptop, Mobile, Tablet)
	brand
	string
	✅
	Brand or manufacturer of the device
	model
	string
	✅
	Model name or number of the device
	os
	string
	✅
	Operating system running on the device (e.g., Windows, iOS)
	serial_number
	string
	✅
	Serial number uniquely identifying the device
	device_password
	string
	✅
	Password or PIN for unlocking the device
	recovery_email
	string
	✅
	Recovery email associated with the device, if any
	recovery_code
	string
	✅
	Recovery code or backup key for the device
	family_note
	string
	✅
	Note for family members about this device
	legacy_note
	string
	✅
	Note about legacy instructions for the device
	created_by
	string
	✅
	Identifier of the user who created this metadata
	created_at
	string
	✅
	Timestamp when this metadata was created
	updated_by
	string
	✅
	Identifier of the user who last updated this metadata
	updated_at
	string
	✅
	Timestamp when this metadata was last updated
	



Nested Type: SubscriptionSub



Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the subscription
	openbaoKeyName
	String
	✅
	The key name used for encryption or access in the vault
	usernameEmail
	String
	✅
	The username or email associated with the subscription
	recoveryEmail
	String
	✅
	The recovery email for the subscription account
	recoveryCode
	String
	✅
	The recovery code for the subscription account
	authType
	String
	✅
	The authentication type (e.g., SMS, App)
	amount
	Double
	✅
	The payment amount for the subscription
	frequency
	String
	✅
	The payment frequency (e.g., monthly, yearly)
	paymentMode
	String
	✅
	The payment mode (e.g., credit card, UPI)
	renewalDate
	String
	✅
	The renewal date for the subscription (null if auto-renewal is off)
	accStatusAfterPassingId
	Int32
	✅
	The ID representing the account status after the user's passing
	subServiceNames
	String
	✅
	The name of the subscription service
	subscriptionsTypes
	String
	✅
	The type of subscription
	legacyNote
	String
	✅
	A note regarding legacy instructions for the subscription
	familyNote
	String
	✅
	A note for family members regarding the subscription
	selectedContactsId
	Int32
	✅
	The ID of selected contacts associated with the subscription
	password
	String
	✅
	The password for the subscription account
	recordIdentifier
	String
	✅
	A unique identifier for the subscription record
	createdBy
	String
	✅
	The identifier of the user who created the subscription
	createdAt
	String
	✅
	The timestamp when the subscription was created
	updatedBy
	String
	✅
	The identifier of the user who last updated the subscription
	updatedAt
	String
	✅
	The timestamp when the subscription was last updated
	

Nested Type: OtherAccDetails


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the other account record
	openbao_key_name
	string
	✅
	Key name used for encryption or vault access
	account_type
	string
	✅
	Type of the account (e.g., Gaming, Streaming, Membership)
	platform_name
	string
	✅
	Name of the platform or service provider
	username
	string
	✅
	Username associated with the account
	password
	string
	✅
	Password for accessing the account
	recovery_email
	string
	✅
	Recovery email linked to the account
	recovery_code
	string
	✅
	Backup code or recovery key for the account
	auth_type
	string
	✅
	Type of authentication (e.g., SMS, App-based 2FA)
	family_note
	string
	✅
	Note for family members about this account
	legacy_note
	string
	✅
	Instructions or notes for legacy access to the account
	acc_status_after_passing_id
	int32
	✅
	ID representing the desired account status after passing
	selected_contacts_id
	int32
	✅
	ID referencing selected contacts who may access this account
	created_by
	string
	✅
	Identifier of the user who created this account record
	created_at
	string
	✅
	Timestamp when the account record was created
	updated_by
	string
	✅
	Identifier of the user who last updated the record
	updated_at
	string
	✅
	Timestamp when the record was last updated
	

Nested Type: EmailDetails


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the email account
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault
	email
	String
	✅
	The email address associated with the account
	password
	String
	✅
	The password for the email account
	recovery_email
	String
	✅
	The recovery email for the account
	recovery_code
	String
	✅
	The recovery code for the account
	auth_type
	String
	✅
	The authentication type (e.g., SMS, App)
	family_note
	String
	✅
	A note for family members regarding the email account
	legacy_note
	String
	✅
	A note regarding legacy instructions for the account
	acc_status_after_passing_id
	Int32
	✅
	The ID representing the account status after the user's passing
	selected_contacts_id
	Int32
	✅
	The ID of selected contacts associated with the account
	created_by
	String
	✅
	The identifier of the user who created the email account record
	created_at
	String
	✅
	The timestamp when the email account record was created
	updated_by
	String
	✅
	The identifier of the user who last updated the email account record
	updated_at
	String
	✅
	The timestamp when the email account record was last updated
	


API: GetDigitalDataBasedOnType
Description: Fetches digital vault data based on the specified type and filters.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user requesting the data.
	personaId
	String
	✅
	ID of the persona associated with the data.
	type
	String
	✅
	Type of data to fetch (e.g., subscription, email).
	vaultId
	Int32
	✅
	Unique identifier of the vault.
	groupId
	Int32
	✅
	Unique identifier of the group.
	moduleId
	Int32
	✅
	Unique identifier of the module.
	recordId
	Int32
	✅
	Unique identifier of the record.
	softRevoke
	String
	✅
	Soft revoke status or flag.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	allSubscriptionSub
	SubscriptionSub[]
	

	List of subscription records.
	allEmailDetails
	EmailDetails[]
	

	List of email account details.
	allSocialMediaRecord
	SocialMediaRecord[]
	

	List of social media records.
	allManageDevicesRecord
	manageDevicesMetaData[]
	

	List of managed device records.
	allPrivateFolderData
	PrivateFolderData[]
	

	List of private folder data.
	AllOtherAccDetails
	OtherAccDetails[]
	

	List of other account details.
	________________


Nested Type: SocialMediaRecord


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the social media account
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault
	platform
	String
	✅
	The social media platform (e.g., Facebook, Twitter)
	username
	String
	✅
	The username associated with the social media account
	password
	String
	✅
	The password for the social media account
	recovery_email
	String
	✅
	The recovery email for the account
	recovery_code
	String
	✅
	The recovery code for the account
	auth_type
	String
	✅
	The authentication type (e.g., SMS, App)
	family_note
	String
	✅
	A note for family members regarding the account
	legacy_note
	String
	✅
	A note regarding legacy instructions for the account
	acc_status_after_passing_id
	Int32
	✅
	The ID representing the account status after the user's passing
	selected_contacts_id
	Int32
	✅
	The ID of selected contacts associated with the account
	created_by
	String
	✅
	The identifier of the user who created the account record
	created_at
	String
	✅
	The timestamp when the account record was created
	updated_by
	String
	✅
	The identifier of the user who last updated the account record
	updated_at
	String
	✅
	The timestamp when the account record was last updated
	Nested Type : manageDevicesMetaData
Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the device metadata entry
	openbao_key_name
	string
	✅
	Key name used for encryption or secure vault access
	device_type
	string
	✅
	Type of device (e.g., Laptop, Mobile, Tablet)
	brand
	string
	✅
	Brand or manufacturer of the device
	model
	string
	✅
	Model name or number of the device
	os
	string
	✅
	Operating system running on the device (e.g., Windows, iOS)
	serial_number
	string
	✅
	Serial number uniquely identifying the device
	device_password
	string
	✅
	Password or PIN for unlocking the device
	recovery_email
	string
	✅
	Recovery email associated with the device, if any
	recovery_code
	string
	✅
	Recovery code or backup key for the device
	family_note
	string
	✅
	Note for family members about this device
	legacy_note
	string
	✅
	Note about legacy instructions for the device
	created_by
	string
	✅
	Identifier of the user who created this metadata
	created_at
	string
	✅
	Timestamp when this metadata was created
	updated_by
	string
	✅
	Identifier of the user who last updated this metadata
	updated_at
	string
	✅
	Timestamp when this metadata was last updated
	



Nested Type: SubscriptionSub



Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the subscription
	openbaoKeyName
	String
	✅
	The key name used for encryption or access in the vault
	usernameEmail
	String
	✅
	The username or email associated with the subscription
	recoveryEmail
	String
	✅
	The recovery email for the subscription account
	recoveryCode
	String
	✅
	The recovery code for the subscription account
	authType
	String
	✅
	The authentication type (e.g., SMS, App)
	amount
	Double
	✅
	The payment amount for the subscription
	frequency
	String
	✅
	The payment frequency (e.g., monthly, yearly)
	paymentMode
	String
	✅
	The payment mode (e.g., credit card, UPI)
	renewalDate
	String
	✅
	The renewal date for the subscription (null if auto-renewal is off)
	accStatusAfterPassingId
	Int32
	✅
	The ID representing the account status after the user's passing
	subServiceNames
	String
	✅
	The name of the subscription service
	subscriptionsTypes
	String
	✅
	The type of subscription
	legacyNote
	String
	✅
	A note regarding legacy instructions for the subscription
	familyNote
	String
	✅
	A note for family members regarding the subscription
	selectedContactsId
	Int32
	✅
	The ID of selected contacts associated with the subscription
	password
	String
	✅
	The password for the subscription account
	recordIdentifier
	String
	✅
	A unique identifier for the subscription record
	createdBy
	String
	✅
	The identifier of the user who created the subscription
	createdAt
	String
	✅
	The timestamp when the subscription was created
	updatedBy
	String
	✅
	The identifier of the user who last updated the subscription
	updatedAt
	String
	✅
	The timestamp when the subscription was last updated
	

Nested Type: OtherAccDetails


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the other account record
	openbao_key_name
	string
	✅
	Key name used for encryption or vault access
	account_type
	string
	✅
	Type of the account (e.g., Gaming, Streaming, Membership)
	platform_name
	string
	✅
	Name of the platform or service provider
	username
	string
	✅
	Username associated with the account
	password
	string
	✅
	Password for accessing the account
	recovery_email
	string
	✅
	Recovery email linked to the account
	recovery_code
	string
	✅
	Backup code or recovery key for the account
	auth_type
	string
	✅
	Type of authentication (e.g., SMS, App-based 2FA)
	family_note
	string
	✅
	Note for family members about this account
	legacy_note
	string
	✅
	Instructions or notes for legacy access to the account
	acc_status_after_passing_id
	int32
	✅
	ID representing the desired account status after passing
	selected_contacts_id
	int32
	✅
	ID referencing selected contacts who may access this account
	created_by
	string
	✅
	Identifier of the user who created this account record
	created_at
	string
	✅
	Timestamp when the account record was created
	updated_by
	string
	✅
	Identifier of the user who last updated the record
	updated_at
	string
	✅
	Timestamp when the record was last updated
	

Nested Type: EmailDetails


Field
	Type
	Required
	Description
	id
	Int32
	✅
	The unique identifier for the email account
	openbao_key_name
	String
	✅
	The key name used for encryption or access in the vault
	email
	String
	✅
	The email address associated with the account
	password
	String
	✅
	The password for the email account
	recovery_email
	String
	✅
	The recovery email for the account
	recovery_code
	String
	✅
	The recovery code for the account
	auth_type
	String
	✅
	The authentication type (e.g., SMS, App)
	family_note
	String
	✅
	A note for family members regarding the email account
	legacy_note
	String
	✅
	A note regarding legacy instructions for the account
	acc_status_after_passing_id
	Int32
	✅
	The ID representing the account status after the user's passing
	selected_contacts_id
	Int32
	✅
	The ID of selected contacts associated with the account
	created_by
	String
	✅
	The identifier of the user who created the email account record
	created_at
	String
	✅
	The timestamp when the email account record was created
	updated_by
	String
	✅
	The identifier of the user who last updated the email account record
	updated_at
	String
	✅
	The timestamp when the email account record was last updated
	

Nested Type : PrivateFolderData


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the private folder
	openbao_key_name
	string
	✅
	Key name used for secure vault encryption or access
	folder_name
	string
	✅
	Name of the private folder
	folder_description
	string
	✅
	Description or purpose of the folder
	folder_password
	string
	✅
	Password required to access the folder
	recovery_email
	string
	✅
	Recovery email associated with the folder
	recovery_code
	string
	✅
	Recovery code for accessing the folder
	family_note
	string
	✅
	Note for family members regarding the folder
	legacy_note
	string
	✅
	Note regarding legacy instructions for the folder
	created_by
	string
	✅
	Identifier of the user who created the folder
	created_at
	string
	✅
	Timestamp when the folder was created
	updated_by
	string
	✅
	Identifier of the user who last updated the folder
	updated_at
	string
	✅
	Timestamp when the folder was last updated
	

API: AddOtherAccount
Description: Adds a new "other" account for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	user_id
	String
	✅
	ID of the user associated with the account.
	otherAccountName
	String
	✅
	Name of the other account.
	emailId
	String
	✅
	Email ID associated with the account.
	accountPassword
	String
	✅
	Password for the account.
	additionalInfo
	String
	

	Additional information about the account.
	files
	OtherAccFile[]
	

	List of files associated with the account.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	id
	Int32
	✅
	Unique identifier for the created account.
	________________


API: GetOtherAccounts
Description: Fetches all "other" accounts for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user whose accounts are fetched.
	🔸 Response Fields (accountList array)
Field
	Type
	Required
	Description
	otherAccID
	Int32
	✅
	Unique identifier for the other account.
	userId
	String
	✅
	ID of the user associated with the account.
	otherAccountName
	String
	✅
	Name of the other account.
	emailId
	String
	✅
	Email ID associated with the account.
	accountPassword
	String
	✅
	Password for the account.
	additionalInfo
	String
	

	Additional information about the account.
	date
	String
	✅
	Creation date of the account.
	OtherAccFiles
	GetOtherAccFile[]
	

	List of files associated with the account.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	createdBy
	String
	✅
	ID of the user who created the entry.
	createdAt
	String
	✅
	Timestamp of when the record was created.
	updatedBy
	String
	✅
	ID of the user who last updated the entry.
	updatedAt
	String
	✅
	Timestamp of the last update.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: GetOtherAccountID
Description: Fetches a specific "other" account by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	OtherAccountId
	Int64
	✅
	Unique identifier of the other account to fetch.
	user_id
	String
	

	ID of the user (optional, for additional context).
	🔸 Response Fields (account)
Field
	Type
	Required
	Description
	other_acc_id
	Int64
	✅
	Unique identifier for the other account.
	user_id
	String
	✅
	ID of the user associated with the account.
	other_account_name
	String
	✅
	Name of the other account.
	email_id
	String
	✅
	Email ID associated with the account.
	account_password
	String
	✅
	Password for the account.
	additional_info
	String
	

	Additional information about the account.
	created_at
	String
	✅
	Creation date of the account (format: dd-mm-yyyy).
	other_acc_files
	GetOtherAccIDFile[]
	

	List of files associated with the account.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


Nested Type: GetOtherAccIDFile


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier for the file record associated with an "Other Account"
	other_acc_id
	int32
	✅
	Reference ID linking this file to the corresponding OtherAccDetails record
	file_name
	string
	✅
	Name of the uploaded file
	file_type
	string
	✅
	MIME type or extension indicating the file format (e.g., PDF, JPG)
	file_url
	string
	✅
	URL or storage location of the file
	created_by
	string
	✅
	Identifier of the user who uploaded the file
	created_at
	string
	✅
	Timestamp when the file was uploaded
	updated_by
	string
	✅
	Identifier of the user who last updated the file information
	updated_at
	string
	✅
	Timestamp when the file information was last updated
	

API: UpdateOtherAcc
Description: Updates an existing "other" account.
🔸 Request Payload
Field
	Type
	Required
	Description
	user_id
	String
	✅
	ID of the user associated with the account.
	otherAccountName
	String
	✅
	Name of the other account.
	emailId
	String
	✅
	Email ID associated with the account.
	additionalInfo
	String
	

	Additional information about the account.
	files
	updateOtherAccFile[]
	

	List of files to be updated for the account.
	OtherAccountId
	Int32
	✅
	Unique identifier of the account to update.
	accountPassword
	String
	✅
	Password for the account.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	recordIdentifier
	String
	✅
	Unique UUID for traceability.
	id
	Int32
	✅
	Unique identifier for the updated account.
	________________


Nested Type :updateOtherAccFile


Field
	Type
	Required
	Description
	id
	int32
	✅
	Unique identifier of the file record to be updated
	other_acc_id
	int32
	✅
	Reference ID of the associated OtherAccDetails record
	file_name
	string
	✅
	New or updated name of the file
	file_type
	string
	✅
	Updated MIME type or file format
	file_url
	string
	✅
	Updated file URL or storage path
	updated_by
	string
	✅
	Identifier of the user performing the update
	updated_at
	string
	✅
	Timestamp when the file was last updated
	

API: DeleteOtherAcc
Description: Deletes a specific "other" account.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the account.
	otherAccountID
	Int64
	✅
	Unique identifier of the other account to delete.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


API: SetCredentialPair
Description: Sets a credential pair for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the credential pair.
	data
	credentialPair[]
	✅
	List of credential pairs to set.
	data.id
	Int32
	✅
	Unique identifier for the credential pair.
	data.pathHash
	String
	✅
	Hash of the path for the credential.
	data.createdBy
	String
	✅
	ID of the user who created the credential pair.
	data.encryptedBlob
	String
	✅
	Encrypted data blob for the credential.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	________________


Nested Type : CredentialPair


Field
	Type
	Required
	Description
	username
	string
	✅
	Username credential for account access
	password
	string
	✅
	Password credential for account access
	



API: GetCredentialPair
Description: Retrieves a credential pair by its path hash.
🔸 Request Payload
Field
	Type
	Required
	Description
	pathHash
	String
	✅
	Hash of the path for the credential to retrieve.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	data.id
	Int32
	✅
	Unique identifier for the credential pair.
	data.pathHash
	String
	✅
	Hash of the path for the credential.
	data.createdBy
	String
	✅
	ID of the user who created the credential pair.
	data.encryptedBlob
	String
	✅
	Encrypted data blob for the credential.
	________________


API: DeleteCredentialPair
Description: Deletes a credential pair by its path hash.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	ID of the user associated with the credential pair.
	pathHash
	String
	✅
	Hash of the path for the credential to delete.
	🔸 Response Fields
Field
	Type
	Required
	Description
	code
	Int32
	✅
	Status code (e.g., HTTP-like status).
	success
	Boolean
	✅
	Indicates success or failure of the request.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if the request fails.
	



























API: Upload
🔸 Request Payload
Field
	Type
	REQUIRED
	Description
	fileContent
	Byte
	✅
	The content of the file to upload.
	fileName
	String
	✅
	The name of the file.
	bucketName
	String
	✅
	The GCS (Google Cloud Storage) bucket name.
	folderName
	String
	✅
	The folder path in the bucket.
	

🔸 Response Fields
Field
	Type
	REQUIRED
	Description
	errorMessage
	String
	

	Error message if upload fails.
	fileURL
	String
	✅
	URL of the uploaded file.
	success
	Boolean
	✅
	Indicates if the upload was successful.
	

API: Fetch
🔸 Request Payload
Field
	Type
	REQUIRED
	Description
	fileName
	String
	

	The name of the file.
	bucketName
	String
	✅
	The GCS (Google Cloud Storage) bucket name.
	fileKey
	String
	✅
	The key/path of the file in the bucket.
	

🔸 Response Fields
Field
	Type
	REQUIRED
	Description
	fileContent
	Byte
	✅
	The content of the fetched file.
	errorMessage
	String
	

	Error message if fetch fails.
	success
	Boolean
	✅
	Indicates if the upload was successful.
	







________________




 
API: legalVault 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	value 
	Boolean 
	✅ 
	Toggle to show/hide LegalVault 
	🔸 Response Fields 
Field 
	Type 
	Required 
	Description 
	errorMessage 
	String 
	 
	Error message if any. 
	success 
	Boolean 
	         ✅ 
	Status of the operation. 
	message 
	String 
	 
	Additional information. 
	code 
	Int 
	 
	Response code. 
	 
 
 
 
API:getAllLastWills 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	userId 
	String 
	 ✅ 
	ID of the user. 
	🔸 Response  
Field 
	Type 
	Description 
	wills 
	[LastWill!] 
	List of last wills 
	success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	 
API:getLastWillByID 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	userId 
	String 
	     ✅ 
	ID of the user. 
	id 
	int 
	     ✅ 
	ID of the will. 
	 
🔸 Response  
Field 
	Type 
	Description 
	wills 
	LastWill 
	 last will details 
	success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	                     error 
	                   String 
	                                     Error if any 
	API:addLastWill 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	userId 
	String 
	 ✅ 
	User ID 
	willTitle 
	String 
	  ✅ 
	Title of the will. 
	notes 
	String 
	 
	Additional Notes 
	flag 
	String 
	 
	Laptop, Mobile Application 
	files 
	[AddLegalFileInput] 
	 
	Attached file array 
	🔸 Response  
Field 
	Type 
	Description 
	id 
	Int 
	 Created Will ID 
	success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	recordIdentifier 
	String 
	Internal record UUID 
	 
API:updateLastWill 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	id 
	Int 
	   ✅ 
	Will ID 
	userId 
	String 
	   ✅ 
	User ID 
	willTitle 
	String 
	   ✅ 
	Title of the will. 
	notes 
	String 
	 
	Additional Notes 
	flag 
	String 
	 
	Laptop, Mobile Application 
	files 
	[AddLegalFileInput] 
	 
	Attached file array 
	 
🔸 Response 
Field 
	Type 
	Description 
	id 
	Int 
	 Created Will ID 
	success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	recordIdentifier 
	String 
	Internal record UUID 
	 
API:deleteLastWill 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	userId 
	String 
	  ✅ 
 
	ID of the user. 
	id 
	int 
	   ✅ 
	ID of the will. 
	🔸 Response 
Field 
	Type 
	Description 
	success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	 
API:getAssetType/getHomeType/getUtilityType 
🔸 Request 
No Input 
🔸 Response 
Field 
	Type 
	Description 
	assetType/homeTypes/utilityType 
	Array 
	Dropdown Values 
	success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	 
 
API:addProperty 
Response  
success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	id 
	Int 
	Property Id 
	recordIdentifier 
	String 
	Internal record Id 
	 
API:updateProperty 
🔸 Request Payload 
Field 
	Type 
	Required 
	Description 
	id 
	Int 
	✅ 
	Property ID 
	userId 
	String 
	                      ✅ 
	User  ID 
	assetType 
	Int 
	 
	Asset type 
	homeType 
	Int 
	 
	Home Type 
	rentAmount 
	float 
	 
	Rent Amount 
	addressLine 
	String 
	 
	Address Line 
	apartmentUnit 
	String 
	 
	Apartment 
	city 
	String 
	 
	City 
	state 
	String 
	 
	State 
	zipCode 
	String 
	 
	Zip Code 
	country 
	String 
	 
	Country 
	utilityType 
	Int 
	 
	Utility Type Id 
	utilitySpecify 
	String 
	 
	Custom utility name 
	accountNumber 
	String 
	 
	Account number 
	companyName 
	String 
	 
	Company Name 
	notes 
	String 
	 
	Additional Notes 
	recordIdentifier 
	String 
	   ✅ 
	Unique Record Id 
	files 
	[PropertyFileInput] 
	 
	List of attached files 
	 
🔸 Response 
success 
	Boolean 
	Status of the operation. 
	message 
	String 
	Status Message. 
	code 
	Int 
	Response code. 
	error 
	String 
	Error if any 
	id 
	Int 
	Property Id 
	recordIdentifier 
	String 
	Internal record Id 
	 








API: countries
Returns a list of all countries available in the system.
🔸 Response Payload


Field
	Type
	Required
	Description
	message
	String
	✅
	Description of the operation outcome.
	success
	Boolean
	✅
	Indicates whether the operation was successful.
	code
	Int
	✅
	HTTP-like status code.
	error
	String
	 
	Error message, if any.
	data
	[Country]
	

	List of country objects.
	



🔹 Nested Type: Country




Field
	Type
	Required
	Description
	id
	Int
	✅
	Country ID.
	Name
	String
	✅
	Country Name.
	states
	[State]
	

	List of States
	



🔹Nested Type: State


Field
	Type
	Required
	Description
	stateId
	Int
	✅
	Unique identifier for the state.
	stateName
	String
	✅
	Name of the state.
	createdAt
	String
	✅
	Timestamp when the state was created.
	createdBy
	String
	 
	User who created the state.
	updatedAt
	String
	✅
	Timestamp when the state was last updated.
	updatedBy
	String
	 
	User who last updated the state.
	status
	Boolean
	 
	Indicates if the state is active or inactive.
	countryId
	Int
	✅
	ID of the associated country.
	country
	Country
	 
	Country object linked to the state.
	API: Country
Retrieves details of a specific country using its ID.
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique ID of the country to retrieve.
	

🔸 Response Payload


Field
	Type
	Required
	Description
	message
	String
	✅
	Description of the operation outcome.
	success
	Boolean
	✅
	Indicates whether the operation was successful.
	code
	Int
	✅
	HTTP-like status code.
	error
	String
	 
	Error message, if any.
	data
	Country
	✅
	Detailed country information.
	



API: States
Returns a list of states that belong to the specified country ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	countryId
	Int
	✅
	ID of the country to list states for.
	 
🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Description of the operation outcome.
	success
	Boolean
	✅
	Indicates whether the operation was successful.
	code
	Int
	✅
	HTTP-like status code.
	error
	String
	 
	Error message, if any.
	data
	[State]
	✅
	Array of state objects.
	

API: State
Fetches details of a specific state based on its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique ID of the state to retrieve.
	 
🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Description of the operation outcome.
	success
	Boolean
	✅
	Indicates whether the operation was successful.
	code
	Int
	✅
	HTTP-like status code.
	error
	String
	 
	Error message, if any.
	data
	State
	✅
	Detailed state information.
	

🔹Nested Type: State


Field
	Type
	Required
	Description
	stateId
	Int
	✅
	Unique identifier for the state.
	stateName
	String
	✅
	Name of the state.
	createdAt
	String
	✅
	Timestamp when the state was created.
	createdBy
	String
	 
	User who created the state.
	updatedAt
	String
	✅
	Timestamp when the state was last updated.
	updatedBy
	String
	 
	User who last updated the state.
	status
	Boolean
	 
	Indicates if the state is active or inactive.
	countryId
	Int
	✅
	ID of the associated country.
	country
	Country
	 
	Country object linked to the state.
	





API: forms
Returns all forms available in the system. 


🔸  Response Payload
Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	data 
	[Form] 
	✅ 
	List of available form objects. 
	



API: form
Returns a specific form based on country and state ID. 
🔸 Request Payload
Field
	Type
	Required
	Description
	countryId 
	Int 
	✅ 
	Country ID for form filtering. 
	stateId 
	Int 
	✅ 
	State ID for form filtering. 
	



🔸 Response Payload


Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	form 
	Form 
	

	The matched form object. 
	API: responses
Returns a list of form responses for a given form ID. 
🔸 Request Payload
Field
	Type
	Required
	Description
	formId 
	Int 
	✅ 
	ID of the form to fetch responses for. 
	

🔸 Response Payload
Field
	Type
	Required
	Description
	id 
	Int 
	✅ 
	Response ID. 
	formId 
	Int 
	✅ 
	Associated form ID. 
	userId 
	Int 
	✅ 
	User who submitted the response. 
	submittedAt 
	String 
	 
	Timestamp of submission. 
	form 
	Form 
	 
	The associated form. 
	details 
	[ResponseDetail] 
	 
	Detailed answers. 
	createdAt 
	String 
	 
	Response creation time. 
	createdBy 
	String 
	 
	Creator of the response. 
	updatedAt 
	String 
	 
	Last update timestamp. 
	updatedBy 
	String 
	 
	Last updater of the response. 
	

API: response
Returns details of a single form response based on its ID. 


🔸 Request Payload


Field
	Type
	Required
	Description
	id 
	Int 
	✅ 
	ID of the form response. 
	🔸 Response Payload


Field
	Type
	Required
	Description
	id 
	Int 
	✅ 
	Response ID. 
	formId 
	Int 
	✅ 
	Associated form ID. 
	userId 
	Int 
	✅ 
	User who submitted the response. 
	submittedAt 
	String 
	 
	Submission timestamp. 
	form 
	Form 
	 
	The associated form. 
	details 
	[ResponseDetail] 
	 
	Detailed answers. 
	createdAt 
	String 
	 
	Response creation timestamp. 
	createdBy 
	String 
	 
	Creator of the response. 
	updatedAt 
	String 
	 
	Update timestamp. 
	updatedBy 
	String 
	 
	Last updater of the response. 
	

🔹 Nested Type: ResponseDetail




Field
	Type
	Required
	Description
	id
	Int
	✅
	Response detail ID.
	responseId
	Int
	✅
	ID of the associated form response.
	questionId
	Int
	✅
	ID of the question being answered.
	answer
	String
	 
	The user's answer to the question.
	response
	FormResponse
	 
	The associated form response.
	question
	Question
	 
	The question being answered.
	createdAt
	String
	 
	Record creation timestamp.
	createdBy
	String
	 
	Creator of the record.
	updatedAt
	String
	 
	Last update timestamp.
	updatedBy
	String
	 
	Last updater of the record.
	

API: getAllMedicalHistory
Returns all medical history records for a user. 


🔸 Request Payload
Field
	Type
	Required
	Description
	userId 
	String 
	✅ 
	ID of the user to retrieve medical history for. 
	

🔸 Response Payload


Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	medicalHistory 
	[MedicalHistory] 
	✅ 
	List of medical history records. 
	

🔹 Nested Type: MedicalHistory


Field
	Type
	Required
	Description
	medicalHistoryId
	Int
	✅
	Unique identifier for the medical history record.
	userId
	String
	✅
	ID of the user the record belongs to.
	typeOfRecordId
	Int
	✅
	ID of the type of medical record.
	recordTypeName
	String
	✅
	Name of the medical record type.
	recordDate
	String
	✅
	Date when the medical record was created.
	documentLink
	String
	✅
	Link to the medical document.
	originalFilename
	String
	✅
	Original name of the uploaded file.
	createdBy
	String
	✅
	User who created the record.
	updatedBy
	String
	 
	User who last updated the record.
	createdAt
	String
	✅
	Record creation timestamp.
	updatedAt
	String
	 
	Record update timestamp.
	status
	Boolean
	✅
	Status of the record (active/inactive).
	otherRecordType
	String
	 
	Other specified record type, if any.
	files
	[NotesFiles]
	 
	Attached files related to the medical record.
	



🔹 Nested Type: NotesFiles
Field
	Type
	Required
	Description
	id
	Int
	 
	Unique identifier of the file.
	documentLink
	String
	 
	Link to the file document.
	originalFileName
	String
	 
	Original name of the file.
	updatedAt
	String
	 
	Last update timestamp of the file.
	

API: getAllDoctors
Returns all doctors associated with a user. 


🔸 Request Payload


Field
	Type
	Required
	Description
	userId 
	String 
	✅ 
	ID of the user to retrieve doctors for. 
	

🔸 Response Payload


Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	doctor 
	[Doctor] 
	✅ 
	List of doctor records. 
	



🔹 Nested Type: Doctor
Field
	Type
	R/O
	Description
	id
	Int
	 
	Internal identifier.
	doctorId
	Int
	✅
	Unique identifier for the doctor.
	userId
	String
	✅
	ID of the user associated with the doctor.
	typeId
	Int
	 
	Type ID of the doctor.
	typeName
	String
	 
	Type name of the doctor.
	doctorName
	String
	✅
	Full name of the doctor.
	contactInformation
	String
	 
	Contact information of the doctor.
	city
	String
	 
	City where the doctor practices.
	state
	String
	 
	State where the doctor practices.
	country
	String
	 
	Country where the doctor practices.
	markAsImportant
	Boolean
	 
	Flag if marked as important.
	createdBy
	String
	 
	User who created the record.
	updatedBy
	String
	 
	User who updated the record.
	createdAt
	String
	 
	Record creation timestamp.
	updatedAt
	String
	 
	Record update timestamp.
	status
	Boolean
	 
	Status of the doctor record.
	doctorType
	String
	✅
	Type of doctor.
	recordIdentifier
	String
	✅
	Unique identifier for the doctor's record.
	

API: getInsuranceById
Returns insurance details for a specific insurance ID and user ID. 


🔸 Request Payload
Field
	Type
	Required
	Description
	insuranceId 
	Int 
	✅ 
	ID of the insurance to retrieve. 
	userID 
	String 
	✅ 
	User ID requesting the data. 
	🔸 Response Payload
Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	data 
	GetInsuranceById 
	✅ 
	Insurance detail data. 
	 
API: getTypeOfHealthInsurance
Returns all available types of health insurance. 


🔸 Response Payload
Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	healthInsuranceTypes 
	[HealthInsuranceType!] 
	✅ 
	List of health insurance types. 
	

🔹 Nested Type: HealthInsuranceType


Field
	Type
	Required
	Description
	insuranceTypeId
	Int
	✅
	Unique identifier for the insurance type.
	insuranceTypeName
	String
	✅
	Name of the health insurance type.
	 API: getTypeOfDoctor
Returns all available types of doctors. 
🔸 Responce Payload
Field
	Type
	Required
	Description
	code 
	Int 
	                 ✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates whether the operation was successful. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	doctorTypes 
	[DoctorType!] 
	✅ 
	List of doctor type records. 
	

🔹 Nested Type: DoctorType


Field
	Type
	Required
	Description
	typeId
	Int
	✅ 
	Unique identifier for the doctor type.
	doctorType
	String
	✅ 
	Descriptive name of the doctor type
	

 API: userAhdForm
Returns AHD form content for a user with questions and answers. 
🔸 Request Payload
Field
	Type
	Required
	Description
	userId 
	String 
	✅ 
	User ID requesting the form. 
	formId 
	Int 
	✅ 
	Form identifier. 
	page 
	Int 
	 
	Page number for pagination. 
	limit 
	Int 
	 
	Page size limit. 
	

🔸 Responce Payload
Field
	Type
	Required
	Description
	title 
	String 
	✅ 
	Form title. 
	description 
	String 
	✅ 
	Form description. 
	questions 
	[ahdQuestions!] 
	✅ 
	List of form questions and answers. 
	

🔹 Nested Type: ahdQuestions


Field
	Type
	Required
	Description
	question 
	String 
	✅ 
	The question text presented in the form. 
	answer 
	String 
	✅ 
	The answer provided by the user. 
	questionType 
	String 
	✅ 
	Type of the question (e.g., text, multiple-choice). 
	questionOptions 
	JSON 
	✅ 
	JSON array of available answer options. 
	required
	Boolean
	

	Indicates whether the question is mandatory for the user to answer.
	

 API: getUserMedicalHistory
Fetches a specific medical history record by its ID. 
🔸 Request Payload
Field
	Type
	Required
	Description
	medicalHistoryId 
	Int 
	                 ✅ 
	Unique medical history ID. 
	🔸 Responce Payload
Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates success of the operation. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	data 
	MedicalHistoryData 
	✅ 
	Detailed medical history data. 
	

🔹 Nested Type: MedicalHistoryData


Field
	Type
	Required
	Description
	medicalHistoryId 
	Int 
	✅ 
	Medical history record ID. 
	userId 
	String 
	✅ 
	User ID associated with the record. 
	typeOfRecord_id 
	Int 
	 
	Record type ID. 
	recordTypeName 
	String 
	 
	Name of the record type. 
	recordDate 
	String 
	 
	Date of the medical record. 
	createdBy 
	String 
	✅ 
	Creator of the record. 
	updatedBy 
	String 
	✅ 
	User who last updated it. 
	createdAt 
	String 
	✅ 
	Creation timestamp. 
	updatedAt 
	String 
	✅ 
	Last updated timestamp. 
	status 
	Boolean 
	✅ 
	Status of the record. 
	files 
	[MedicalHistoryFile!] 
	✅ 
	Attached medical documents. 
	 
🔹 Nested Type: MedicalHistoryFile 
Field
	Type
	Required
	Description
	fileId 
	Int 
	                 ✅ 
	Unique file identifier. 
	documentLink 
	String 
	 
	Link to the document. 
	originalFilename 
	String 
	 
	Original file name. 
	createdBy 
	String 
	 
	User who uploaded the file. 
	updatedBy 
	String 
	 
	User who updated the file. 
	createdAt 
	String 
	 
	Timestamp of creation. 
	updatedAt 
	String 
	 
	Timestamp of last update. 
	

 API: getDoctorById
Retrieves a specific doctor record for a user. 
🔸 Request Payload
Field
	Type
	Required
	Description
	doctorId 
	Int 
	✅ 
	Doctor's ID. 
	userId 
	String 
	✅ 
	User ID requesting the doctor record. 
	

🔸 Responce Payload
Field
	Type
	Required
	Description
	code 
	Int 
	✅ 
	Status code. 
	success 
	Boolean 
	✅ 
	Indicates success of the operation. 
	message 
	String 
	✅ 
	Operation result message. 
	error 
	String 
	 
	Error message, if any. 
	doctor 
	DoctorData 
	✅ 
	Detailed doctor data. 
	 
🔹 Nested Type: DoctorData
Field
	Type
	Required
	Description
	doctorId 
	Int 
	✅ 
	Doctor ID. 
	userId 
	String 
	✅ 
	Associated user ID. 
	typeId 
	Int 
	✅ 
	Type ID for the doctor. 
	typeName 
	String 
	✅ 
	Name of the doctor's specialization. 
	doctorName 
	String 
	✅ 
	Doctor's full name. 
	contactInformation 
	String 
	 
	Contact information. 
	city 
	String 
	 
	City location. 
	state 
	String 
	 
	State location. 
	country 
	String 
	 
	Country location. 
	markAsImportant 
	Boolean 
	 
	Flag for priority. 
	createdBy 
	String 
	✅ 
	Creator of the record. 
	updatedBy 
	String 
	✅ 
	Last updater. 
	createdAt 
	String 
	✅ 
	Creation timestamp. 
	updatedAt 
	String 
	✅ 
	Last update timestamp. 
	recordIdentifier 
	String 
	✅ 
	Unique record reference. 
	

 API: getHealthInsurancesByUserId
Fetches a list of health insurance records for a specific user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	                 ✅
	User's unique ID.
	

🔸 Responce Payload


Field
	Type
	Required
	Description
	healthInsurances
	[HealthInsurance!]
	✅
	Array of health insurance records.
	message
	String
	✅
	Operation result message.
	error
	String
	 
	Error message, if any.
	code
	Int
	✅
	Status code.
	success
	Boolean
	✅
	Indicates success of the operation.
	🔹 Nested Type: HealthInsurance
Field
	Type
	Required
	Description
	id
	Int
	 
	ID of the record.
	insuranceId
	Int
	✅
	Insurance ID.
	insuranceTypeId
	Int
	✅
	Insurance Type ID.
	insuranceTypeName
	String
	 
	Name of the insurance type.
	userId
	String
	✅
	User ID.
	memberName
	String
	 
	Name of the member.
	memberId
	String
	 
	Member ID.
	groupId
	String
	 
	Group ID.
	dependents
	[String!]
	 
	List of dependents.
	documentLink
	[String!]
	 
	Document URLs.
	originalFilename
	[String!]
	 
	Original file names.
	fileIds
	[Int!]
	✅
	File IDs.
	createdBy
	String
	 
	Creator of the record.
	updatedBy
	String
	 
	Last updater.
	createdAt
	String
	✅
	Record creation date.
	updatedAt
	String
	✅
	Last update date.
	status
	Boolean
	✅
	Record status.
	files
	[NotesFiles!]
	✅
	Attached files.
	recordIdentifier
	String
	✅
	Record identifier.
	

🔹Nested Type: NotesFiles
Field
	Type
	Required
	Description
	id
	Int
	 
	File ID.
	documentLink
	String
	✅
	Link to the document.
	originalFileName
	String
	✅
	Original file name.
	updatedAt
	String
	✅
	Last update timestamp.
	 API: getMedicationsByUserId
Fetches a paginated list of medication records by user ID.


🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	                ✅
	User's unique ID.
	page
	Int
	 
	Page number.
	limit
	Int
	 
	Number of records/page.
	

🔸 Responce Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Operation result message.
	success
	Boolean
	✅
	Operation success flag.
	totalRecords
	Int
	✅
	Total number of records.
	totalPages
	Int
	✅
	Total pages.
	currentPage
	Int
	✅
	Current page.
	code
	Int
	✅
	Status code.
	error
	String
	 
	Error message if any.
	data
	[MedicationRecord!]
	✅
	List of medication records.
	🔹Nested Type: MedicationRecord
Field
	Type
	Required
	Description
	id
	Int
	 
	Record ID.
	medicationId
	Int
	✅
	Medication ID.
	userId
	String
	✅
	User ID.
	treatmentName
	String
	 
	Name of treatment.
	purpose
	String
	 
	Purpose of medication.
	medicineName
	String
	 
	Name of the medicine.
	dosage
	String
	 
	Dosage prescribed.
	startDate
	String
	 
	Start date.
	endDate
	String
	 
	End date.
	frequencyDosage
	String
	 
	Dosage frequency.
	sideEffect
	String
	 
	Side effects if any.
	createdBy
	String
	✅
	Created by.
	updatedBy
	String
	✅
	Updated by.
	status
	Boolean
	✅
	Record status.
	createdAt
	String
	✅
	Creation timestamp.
	updatedAt
	String
	✅
	Update timestamp.
	files
	[medicationFiles]
	 
	Attached medication files.
	recordIdentifier
	String
	✅
	Record ID.
	markAsImportant
	Boolean
	 
	Flag for importance.
	🔹Nested Type: MedicationFiles
Field
	Type
	Required
	Description
	id
	Int
	

	File ID.
	documentLink
	String
	✅
	Link to the document.
	originalFileName
	String
	✅
	Original file name.
	updatedAt
	String
	✅
	Last updated timestamp.
	

 API: getNotesByUserId
Fetches all notes associated with a user ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	               ✅
	User's ID.
	🔸 Responce Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Result message.
	success
	Boolean
	✅
	Operation success status.
	code
	Int
	✅
	Status code.
	error
	String
	 
	Error message if any.
	data
	[Note!]
	✅
	List of notes.
	

🔹Nested Type: Note
Field
	Type
	Required
	Description
	id
	Int
	 
	ID of the note.
	noteId
	Int
	✅
	Note ID.
	userId
	String
	✅
	User ID.
	noteContent
	String
	 
	Note content.
	createdBy
	String
	✅
	Creator.
	updatedBy
	String
	✅
	Last updater.
	createdAt
	String
	✅
	Creation time.
	updatedAt
	String
	✅
	Last updated time.
	markAsImportant
	Boolean
	 
	Importance flag.
	status
	Boolean
	✅
	Status.
	files
	[NotesFiles!]
	✅
	Files attached.
	recordIdentifier
	String
	✅
	Unique record ID.
	

🔹Nested Type: NotesFiles
Field
	Type
	Required
	Description
	id
	Int
	 
	File ID.
	documentLink
	String
	✅
	Link to the document.
	originalFileName
	String
	✅
	Original file name.
	updatedAt
	String
	✅
	Last update timestamp.
	 API: getNotesById
Fetches a specific note by its ID and user ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	notesId
	Int
	✅
	Note ID.
	userId
	String
	✅
	User's ID.
	

🔸 Responce Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Result message.
	success
	Boolean
	✅
	Operation status.
	code
	Int
	✅
	Status code.
	error
	String
	 
	Error if any.
	data
	Note
	✅
	Note record.
	

🔹Nested Type: Note
Field
	Type
	Required
	Description
	id
	Int
	

	ID of the note.
	noteId
	Int
	✅
	Unique identifier for note.
	userId
	String
	✅
	Associated user ID.
	noteContent
	String
	

	Content of the note.
	createdBy
	String
	✅
	User who created the note.
	updatedBy
	String
	✅
	User who last updated the note.
	createdAt
	String
	✅
	Note creation timestamp.
	updatedAt
	String
	✅
	Last updated timestamp.
	markAsImportant
	Boolean
	

	Whether marked important.
	status
	Boolean
	

	Status of the note.
	files
	[NotesFiles!]
	✅
	List of attached files.
	recordIdentifier
	String
	✅
	Unique record reference.
	

🔹Nested Type: NotesFiles
Field
	Type
	Required
	Description
	id
	Int
	

	File ID.
	documentLink
	String
	✅
	Link to the document.
	originalFileName
	String
	✅
	Original file name.
	updatedAt
	String
	✅
	Last updated timestamp.
	

 API: getMedicationById
Fetches a medication record by its ID and associated user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID associated with record
	id
	Int
	✅
	Medication record ID
	🔸 Responce Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Operation result message
	success
	Boolean
	✅
	Indicates success of the operation
	code
	Int
	✅
	Status code
	error
	String
	

	Error message, if any
	data
	MedicationRecord
	✅
	Medication record details
	

🔹Nested Type: MedicationRecord
Field
	Type
	Required
	Description
	id
	Int
	

	Internal ID
	medicationId
	Int
	✅
	Medication ID
	userId
	String
	✅
	User ID
	treatmentName
	String
	

	Treatment name
	purpose
	String
	

	Purpose of medication
	medicineName
	String
	

	Medicine name
	dosage
	String
	

	Dosage
	startDate
	String
	

	Start date
	endDate
	String
	

	End date
	frequencyDosage
	String
	

	Frequency of dosage
	sideEffect
	String
	

	Side effects
	createdBy
	String
	✅
	Created by
	updatedBy
	String
	✅
	Last updated by
	status
	Boolean
	✅
	Record status
	createdAt
	String
	✅
	Record creation date
	updatedAt
	String
	✅
	Record last update date
	files
	[medicationFiles]
	

	Attached files
	recordIdentifier
	String
	✅
	Record identifier
	markAsImportant
	Boolean
	

	Marked as important
	🔹Nested Type: medicationFiles
Field
	Type
	Required
	Description
	id
	Int
	

	File ID
	documentLink
	String
	

	URL to the document
	originalFileName
	String
	

	Original uploaded name
	updatedAt
	String
	

	Last updated timestamp
	 API: getAllergy
Fetches a specific allergy record by its ID and user ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	allergieId
	Int
	✅
	Allergy ID
	userID
	String
	✅
	User ID associated
	🔸 Responce Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Operation result message
	success
	Boolean
	✅
	Indicates success of the operation
	code
	Int
	✅
	Status code
	error
	String
	

	Error message, if any
	data
	Allergy
	✅
	Detailed allergy information
	🔹Nested Type: Allergy
Field
	Type
	Required
	Description
	id
	Int
	

	Internal ID
	allergieId
	Int
	✅
	Allergy ID
	userId
	String
	✅
	User ID
	allergyTypeId
	Int
	

	Type ID
	allergyTypeName
	String
	

	Type name
	description
	String
	

	Allergy description
	treatment
	String
	

	Treatment info
	additionalInfo
	String
	

	Additional information
	serverityId
	Int
	

	Severity ID
	serverityType
	String
	

	Severity type
	reactions
	String
	

	Recorded reactions
	createdBy
	String
	✅
	Created by
	updatedBy
	String
	✅
	Last updated by
	createdAt
	String
	✅
	Created timestamp
	updatedAt
	String
	✅
	Updated timestamp
	status
	Boolean
	✅
	Record status
	files
	[AllergyFile]
	

	Related files
	recordIdentifier
	String
	✅
	Record identifier
	markAsImportant
	String
	

	Marked important or not
	🔹Nested Type: AllergyFile
Field
	Type
	Required
	Description
	fileId
	Int
	✅
	File ID
	allergieId
	Int
	✅
	Related allergy ID
	documentLink
	String
	

	URL to the document
	originalFilename
	String
	

	Original uploaded name
	createdBy
	String
	✅
	Created by
	updatedBy
	String
	✅
	Updated by
	createdAt
	String
	✅
	Created timestamp
	updatedAt
	String
	✅
	Updated timestamp
	status
	Boolean
	✅
	File status
	 API: getAllergiesByUserId
Returns paginated list of allergies for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	page
	Int
	

	Page number
	limit
	Int
	

	Items per page
	🔸 Response Payload
Field
	Type
	Required
	Description
	allergies
	[Allergy!]
	✅
	List of allergy records
	totalCount
	Int
	✅
	Total number of allergy records
	currentPage
	Int
	✅
	Current page number
	totalPages
	Int
	✅
	Total number of pages
	recordsInCurrentPage
	Int
	✅
	Count in current page
	message
	String
	✅
	Operation result message
	success
	Boolean
	✅
	Indicates success of the operation
	code
	Int
	✅
	Status code
	error
	String
	

	Error message, if any
	🔹Nested Type: Allergy
Field
	Type
	Required
	Description
	id
	Int
	

	Internal ID
	allergieId
	Int
	✅
	Allergy ID
	userId
	String
	✅
	User ID
	allergyTypeId
	Int
	

	Type ID
	allergyTypeName
	String
	

	Type name
	description
	String
	

	Allergy description
	treatment
	String
	

	Treatment info
	additionalInfo
	String
	

	Additional information
	serverityId
	Int
	

	Severity ID
	serverityType
	String
	

	Severity type
	reactions
	String
	

	Recorded reactions
	createdBy
	String
	✅
	Created by
	updatedBy
	String
	✅
	Last updated by
	createdAt
	String
	✅
	Created timestamp
	updatedAt
	String
	✅
	Updated timestamp
	status
	Boolean
	✅
	Record status
	files
	[AllergyFile]
	

	Related files
	recordIdentifier
	String
	✅
	Record identifier
	markAsImportant
	String
	

	Marked important or not
	🔹Nested Type: AllergyFile
Field
	Type
	Required
	Description
	fileId
	Int
	✅
	File ID
	allergieId
	Int
	✅
	Related allergy ID
	documentLink
	String
	

	URL to the document
	originalFilename
	String
	

	Original uploaded name
	createdBy
	String
	✅
	Created by
	updatedBy
	String
	✅
	Updated by
	createdAt
	String
	✅
	Created timestamp
	updatedAt
	String
	✅
	Updated timestamp
	status
	Boolean
	✅
	File status
	

 API: getTypeOfAllergies
Returns a list of all predefined allergy types configured in the system.
🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code.
	success
	Boolean
	✅
	Indicates if request was successful.
	message
	String
	✅
	Informational message.
	allergyTypes
	[AllergyType!]
	✅
	List of all allergy types.
	error
	String
	

	Error message if any.
	🔹Nested Type: AllergyType
Field
	Type
	Required
	Description
	typeId
	Int
	✅
	Unique ID for the allergy type.
	allergyType
	String
	✅
	Name of the allergy.
	 API: getBloodGroup
🔸 Response Payload


Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code.
	success
	Boolean
	✅
	Indicates if request was successful.
	message
	String
	✅
	Informational message.
	bloodGroup
	[BloodGroup!]
	✅
	List of blood group options.
	error
	String
	

	Error message if any.
	🔹Nested Type: BloodGroup
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique ID for the blood group.
	bloodGroup
	String
	✅
	Name of the blood group (e.g., A+).
	

 API: getRelationship
Returns a list of supported relationship types (e.g., Father, Mother, Guardian) for form-related questions.
🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code.
	success
	Boolean
	✅
	Indicates if request was successful.
	message
	String
	✅
	Informational message.
	relationships
	[Relationship!]
	✅
	List of relationship options.
	error
	String
	

	Error message if any.
	🔹Nested Type: Relationship
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique ID of the relationship.
	relationship
	String
	✅
	Name of the relationship (e.g., Father).
	

 API: getUserMedicalResponses
Returns all saved medical form responses of a user for a specific section. Includes metadata like health status, blood group, attached files, and emergency indicators.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique ID of the user.
	sectionId
	Int
	✅
	ID of the form section.
	🔸 Response Payload
Field
	Type
	Required
	Description
	id
	Int
	

	Record ID.
	userId
	String
	✅
	ID of the user.
	sectionId
	Int
	✅
	Section identifier.
	bloodGroupId
	Int
	✅
	ID of selected blood group.
	bloodGroupName
	String
	✅
	Name of selected blood group.
	name
	String
	

	User's name (optional).
	age
	Int
	

	User's age (optional).
	generalHealth
	String
	

	General health condition described by user.
	responses
	[QuestionResponse!]
	✅
	List of answers submitted by user.
	🔹Nested Type: QuestionResponse
Field
	Type
	Required
	Description
	questionId
	Int
	✅
	Unique ID of the question.
	questionType
	String
	✅
	Type of question (text, checkbox, etc.).
	question
	String
	✅
	Text of the question.
	relationIds
	String
	

	Relationship IDs in comma-separated format.
	responseValue
	ResponsevalueStructure
	✅
	Structure representing user's answer.
	hasMedicalCondition
	String
	

	Indicates if a medical condition was reported.
	emergencyAlert
	Boolean
	

	True if marked as an emergency condition.
	options
	String
	

	Options shown to user (if applicable).
	files
	[userResponseFiles]
	

	Any documents/files attached by the user.
	relationshipNames
	[String!]
	✅
	List of names matched with the relationIds provided.
	CreatedAt
	String
	

	Timestamp of when this response was created.
	🔹Nested Type: userResponseFiles
Field
	Type
	Required
	Description
	fileId
	Int
	✅
	Unique ID of the file.
	documentLink
	String
	

	Link to view or download the file.
	originalFilename
	String
	

	Name of the file uploaded by the user.
	updatedAt
	String
	

	Timestamp when the file was last modified.
	

 API: getUserMedicalAndEmergencyResponses
Returns medical and emergency question responses submitted by a user for a given section.
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique ID of the user.
	sectionId
	Int
	✅
	ID of the section to be fetched.
	🔸 Response Payload
Field
	Type
	Required
	Description
	id
	Int
	✅
	Response record ID.
	userId
	String
	✅
	ID of the user.
	sectionId
	Int
	✅
	Section identifier.
	name
	String
	✅
	Name of the user.
	age
	Int
	✅
	Age of the user.
	bloodGroup
	String
	✅
	User's blood group.
	generalHealth
	String
	✅
	Description of general health.
	medicalResponses
	[QuestionResponses!]
	✅
	Regular medical form responses.
	emergencyMedicalResponses
	[QuestionResponses!]
	✅
	Emergency form responses.
	recordIdentifier
	String
	✅
	Unique identifier for the form record.
	🔹Nested Type: QuestionResponses
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique ID of this response.
	questionId
	Int
	✅
	ID of the question.
	question
	String
	

	Text of the question.
	questionType
	String
	

	Type of the question.
	options
	String
	

	Available options.
	relationIds
	String
	

	Related relationship IDs.
	hasMedicalCondition
	String
	

	Whether user has medical condition (Yes/No).
	emergencyAlert
	Boolean
	

	Emergency alert triggered or not.
	responseValue
	MedicalResponseValueStructure
	✅
	User's answer (custom structure).
	files
	[userResponseFiles]
	

	Attached files.
	recordIdentifier
	String
	✅
	Unique record identifier.
	updatedAt
	String
	✅
	Timestamp of update.
	relationshipNames
	[String!]
	✅
	Names linked to relationship IDs.
	

🔹Nested Type: userResponseFiles
Field
	Type
	Required
	Description
	fileId
	Int
	✅
	Unique identifier for the file.
	documentLink
	String
	

	URL to access the document.
	originalFilename
	String
	

	Original file name.
	updatedAt
	String
	

	Last update timestamp.
	🔹Nested Type: MedicalResponseValueStructure
Field
	Type
	Required
	Description
	type
	String
	

	Type of input used (e.g., "text", "checkbox", etc.).
	text
	String
	

	Free-text answer input by the user.
	options
	[String]
	

	All available options shown to the user.
	selected
	[String]
	

	Options selected by the user (if multiple-choice type).
	

 API: getFamilyMedicalHistoryResponses
Returns saved family medical history responses of a user for a specific section.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique ID of the user.
	sectionId
	Int
	✅
	ID of the section.
	🔸 Response Payload
Field
	Type
	Required
	Description
	id
	Int
	

	Record ID.
	userId
	String
	✅
	User ID.
	sectionId
	Int
	✅
	Section ID.
	bloodGroupId
	Int
	✅
	Blood group ID.
	bloodGroupName
	String
	✅
	Name of the blood group.
	name
	String
	

	Name of the user.
	age
	Int
	

	Age of the user.
	generalHealth
	String
	

	General health description.
	responses
	[QuestionResponse!]
	✅
	Family medical history responses.
	🔹Nested Type: QuestionResponse
Field
	Type
	Required
	Description
	questionId
	Int
	✅
	ID of the question.
	questionType
	String
	✅
	Question type.
	question
	String
	✅
	The question text.
	relationIds
	String
	

	Comma-separated relation IDs.
	responseValue
	ResponsevalueStructure
	✅
	Answer structure.
	hasMedicalCondition
	String
	

	Yes/No value for medical condition.
	emergencyAlert
	Boolean
	

	Flag for emergency concern.
	options
	String
	

	Options for multiple choice.
	files
	[userResponseFiles]
	

	Any uploaded documents.
	relationshipNames
	[String!]
	✅
	Relationship names list.
	CreatedAt
	String
	

	Record creation time.
	🔹Nested Type: userResponseFiles
Field
	Type
	Required
	Description
	fileId
	Int
	✅
	Unique identifier for the file.
	documentLink
	String
	

	URL to access the document.
	originalFilename
	String
	

	Original file name.
	updatedAt
	String
	

	Last update timestamp.
	 API: getAllQuestionsFromSection
Returns all questions configured in a form section, including nested sub-questions, metadata, and user details.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	GetAllQuestionsFromSectionInput
	✅
	Input object for section data
	🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	HTTP status code.
	success
	Boolean
	✅
	Indicates request success.
	message
	String
	✅
	Informational message.
	error
	String
	

	Error message if failed.
	questions
	[QuestionsFromSectionResponse!]
	✅
	All questions and sub-questions.
	ahdUserPersonalDetails
	AhdUserPersonalDetails
	✅
	User metadata.
	recordIdentifier
	String
	✅
	Identifier for the current form.
	

🔹Nested Type: QuestionsFromSectionResponse
Field
	Type
	Required
	Description
	id
	Int
	✅
	Question ID.
	sectionId
	Int
	✅
	Section ID.
	stateId, countryId
	Int
	

	Region identifiers.
	questionHeader
	String
	✅
	Question title.
	questionDescription
	String
	✅
	Detailed question text.
	questionType
	String
	✅
	Type (text, checkbox, etc.).
	questionOptions
	[String!]
	✅
	List of answer choices.
	contactId
	[Int!]
	✅
	Related contacts.
	relatedToId
	Int
	✅
	Linked entity ID.
	agentTypeId
	Int
	✅
	Agent type ID.
	relatedTo
	String
	

	Related entity name.
	agentTypeName
	String
	

	Agent type name.
	createdBy, updatedBy
	String
	✅
	Audit trail.
	createdAt, updatedAt
	String
	✅
	Timestamps.
	subQuestions
	[SubQuestionResponse!]
	✅
	List of sub-questions.
	responseValue
	String
	✅
	Captured response.
	responseText
	String
	✅
	Human-readable answer.
	keys
	String
	✅
	Internal keys.
	skipIndex
	Boolean
	✅
	Whether to skip indexing.
	defaultChecked
	String
	✅
	Default selected value.
	isCollapsed
	Boolean
	✅
	UI collapsed state.
	

🔹Nested Type: SubQuestionResponse
Field
	Type
	Required
	Description
	id
	Int
	✅
	Sub-question ID.
	parentQuestionId
	Int
	✅
	Associated parent question.
	subQuestionHeader
	String
	✅
	Sub-question title.
	subQuestionDescription
	String
	✅
	Description.
	subQuestionType
	String
	✅
	Input type.
	options
	[String!]
	✅
	Option list.
	relatedToId
	Int
	✅
	Related entity ID.
	agentTypeId
	Int
	✅
	Related agent type.
	relatedTo
	String
	

	Related entity name.
	agentTypeName
	String
	

	Agent type name.
	createdAt, updatedAt
	String
	✅
	Timestamps.
	createdBy, updatedBy
	String
	✅
	Audit metadata.
	subResponseValue
	String
	✅
	Answer value.
	keys
	String
	✅
	Key mapping.
	skipIndex
	Boolean
	✅
	Search visibility.
	defaultChecked
	String
	✅
	Default UI checked option.
	isCollapsed
	Boolean
	✅
	Collapsed state.
	contactId
	[Int!]
	✅
	Contact associations.
	🔹Nested Type: AhdUserPersonalDetails
Field
	Type
	Required
	Description
	id, personalDetailsId
	Int
	✅
	Internal IDs.
	userId
	String
	✅
	Associated user ID.
	fullName
	String
	✅
	Full name.
	streetNameAndNumber
	String
	✅
	Street address.
	apartmentNumber, city
	String
	✅
	Address parts.
	pincode, stateId, countryId
	Int
	✅
	Geographic info.
	signedAhdBefore
	Boolean
	✅
	AHD signature history.
	declarationDate
	String
	✅
	Date of declaration.
	institutionName
	String
	✅
	Associated institution.
	selectedSections
	String
	✅
	Sections selected.
	completionStatus
	String
	✅
	Completion state.
	createdAt, updatedAt
	String
	✅
	Record audit timestamps.
	createdBy, updatedBy
	String
	✅
	User audit trail.
	stateName, countryName
	String
	✅
	Location names.
	 API: getSections
Returns all available medical/emergency sections for a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to fetch sections
	🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Response message
	success
	Boolean
	✅
	Indicates success of the operation
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	sections
	[Section]
	✅
	List of section details
	

🔹Nested Type: Section
Field
	Type
	Required
	Description
	id
	Int
	✅
	Section ID
	sectionName
	String
	✅
	Title of the section
	sectionDescription
	String
	✅
	Description of the section
	lastUpdated
	String
	✅
	Last update timestamp
	 API: getFilledSections
Returns sections that have been filled by a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID to fetch sections
	🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Response message
	success
	Boolean
	✅
	Indicates success of the operation
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	sections
	[Section]
	✅
	List of section details
	

🔹Nested Type: Section
Field
	Type
	Required
	Description
	id
	Int
	✅
	Section ID
	sectionName
	String
	✅
	Title of the section
	sectionDescription
	String
	✅
	Description of the section
	lastUpdated
	String
	✅
	Last update timestamp
	 API: getSubmittedSection
Returns all responses submitted for a specific section by the user.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	GetSubmittedSectionInput
	               ✅
	Includes userId and sectionId info
	🔸 Response Payload
Field
	Type
	Required
	Description
	errorMessage
	String
	✅
	Error message, if any
	success
	Boolean
	✅
	Operation status
	message
	String
	✅
	Operation result message
	code
	Int
	✅
	Status code
	responses
	[SubmittedSection]
	✅
	User's submitted answers
	personalDetailsId
	Int
	✅
	ID linking to personal details
	stateId
	Int
	✅
	User’s state ID
	countryId
	Int
	✅
	User’s country ID
	declarationDate
	String
	✅
	Date of submission
	fullName
	String
	✅
	User’s full name
	streetNameAndNumber
	String
	✅
	Street address
	city
	String
	✅
	City name
	apartmentNumber
	String
	✅
	Apartment/flat number
	pincode
	String
	✅
	Area pincode
	signedAhdBefore
	Boolean
	✅
	Whether user signed AHD previously
	institutionName
	String
	✅
	Name of the institution
	selectedSections
	String
	✅
	Section identifiers
	completionStatus
	String
	✅
	Status of section completion
	createdAt
	String
	✅
	Record creation timestamp
	updatedAt
	String
	✅
	Last update timestamp
	createdBy
	String
	✅
	Created by
	updatedBy
	String
	✅
	Updated by
	userId
	String
	✅
	ID of the user
	

🔹Nested Type: SubmittedSection
Field
	Type
	Required
	Description
	id
	Int
	✅
	Record ID
	personalDetailsId
	Int
	✅
	Link to personal detail record
	questionId
	Int
	✅
	Main question ID
	subQuestionId
	Int
	✅
	Sub-question ID
	sectionId
	Int
	✅
	Associated section
	responseValue
	String
	✅
	Answer to main question
	subResponseValue
	String
	✅
	Answer to sub-question
	contactId
	Int
	✅
	Contact associated with response
	relatedToId
	Int
	✅
	Related entity ID
	agentTypeId
	Int
	✅
	Agent type (doctor, hospital, etc.)
	createdAt
	String
	✅
	Creation timestamp
	updatedAt
	String
	✅
	Last updated timestamp
	createdBy
	String
	✅
	Record created by
	updatedBy
	String
	✅
	Record last updated by
	API: GetHealthprogressbar
Returns progress bar status based on filled submodules for the health section.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	Progressbarinput
	✅
	Contains userId/details
	🔸 Response Payload
Field
	Type
	Required
	Description
	submodules
	[VaultAndGroups]
	✅
	Vault progress structure
	message
	String
	✅
	Result message
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation status
	API: getStates
Returns all states and their associated countries.
🔸 Response Payload
Field
	Type
	Required
	Description
	states
	[StateWithCountry]
	✅
	List of states with country
	message
	String
	✅
	Response message
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation status
	

🔹Nested Type: StateWithCountry
Field
	Type
	Required
	Description
	stateId
	Int
	✅
	State ID
	stateName
	String
	✅
	State name
	countryId
	Int
	✅
	Country ID
	countryName
	String
	✅
	Country name
	

 API: listAllAhdContacts
Returns all emergency or personal AHD contacts associated with the user.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	ListAllAhdContactsInput
	✅
	Includes userId or pagination
	🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation status
	message
	String
	✅
	Operation message
	error
	String
	

	Error message, if any
	contacts
	[AllAhdContacts]
	✅
	List of AHD contacts
	

🔹Nested Type: AllAhdContacts
Field
	Type
	Required
	Description
	id
	Int
	✅
	Contact ID
	userId
	String
	✅
	User associated with contact
	contactName
	String
	✅
	Contact person's name
	phoneNumber
	String
	✅
	Contact phone number
	emailId
	String
	✅
	Contact email
	createdBy
	String
	✅
	Record created by
	updatedBy
	String
	✅
	Record last updated by
	createdAt
	String
	✅
	Record creation time
	updatedAt
	String
	✅
	Record last update time
	

 API: getSeverity
Returns all available severity levels.
🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation success status
	message
	String
	✅
	Operation message
	error
	String
	

	Error message
	Severity
	[Severity]
	✅
	List of severity types
	

🔹Nested Type: Severity
Field
	Type
	Required
	Description
	id
	Int
	✅
	Severity ID
	SeverityType
	String
	✅
	Label of severity
	

 API: getSelectedSections
Returns the list of currently selected sections by a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	GetSelectedSectionsRequest
	✅
	User-related input to fetch selected sections
	

🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Operation result message
	success
	Boolean
	✅
	Indicates if the request was successful
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	selectedSections
	[SelectedSection]
	✅
	List of selected sections
	

🔹Nested Type: SelectedSection
Field
	Type
	Required
	Description
	id
	Int
	✅
	Section ID
	sectionName
	String
	✅
	Name of the section
	sectionDescription
	String
	✅
	Description of the section
	

 API: printPdfHealth
Generates and returns a printable PDF containing the user’s complete health profile and records.
🔸 Request Payload
Field
	Type
	Required
	Description
	request
	PrintPdfHealthRequestInput
	                 ✅
	Input including userId and options for PDF generation
	

🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Operation result message
	success
	Boolean
	✅
	Operation status
	code
	Int
	✅
	Response code
	error
	String
	



	Error message
	doctors
	[Doctor]
	✅
	List of associated doctors
	medicalhistory
	MedicalUserResponse
	✅
	Medical history of the user
	medicationAllergies
	[MedicationRecord]
	✅
	Medication allergy records
	healthInsurances
	[HealthInsurance]
	✅
	Health insurance details
	notes
	[Note]
	✅
	User notes
	questions
	[QuestionsFromSectionResponse]
	✅
	Question-answer details
	ahdUserPersonalDetails
	AhdUserPersonalDetails
	✅
	User’s personal details
	myEmergencyContacs
	[ContactDetails]
	✅
	Emergency contact list
	allergies
	[Allergy]
	✅
	List of user allergies
	supplements
	[Supplement]
	✅
	Supplement intake details
	medicalPoa
	[MymedicalPoaResponseData]
	✅
	Medical POA records
	familyMedicalResponses
	[QuestionResponses]
	✅
	Family medical responses
	familyEmergencyMedicalResponses
	[QuestionResponses]
	✅
	Emergency-related responses
	familyMedicalUserResponse
	MedicalUserResponse
	✅
	Complete family medical response
	healthCareAccountIds
	[HealthAccountInfo]
	✅
	Linked healthcare accounts
	vaultName
	String
	✅
	Vault where the data is stored
	medicalhistoryForm
	UserResponses
	✅
	Health form values
	

 API: getMedicalUserResponseById
Returns the user’s medical responses and metadata for a specific ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User's ID
	id
	Int
	✅
	Medical response ID
	

🔹 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Status message
	success
	Boolean
	✅
	Indicates success
	code
	Int
	✅
	Response code
	error
	String
	

	Error details
	singleData
	singleDataUserResponse
	✅
	Basic medical details
	data
	SinglemedicalUserResponse
	✅
	Medical question response
	

🔹Nested Type: singleDataUserResponse
Field
	Type
	Required
	Description
	userId
	String
	✅
	User ID
	sectionId
	Int
	✅
	Section ID
	bloodGroup
	String
	

	Blood group name
	bloodGroupId
	Int
	✅
	Blood group ID
	name
	String
	

	Name of the user
	age
	Int
	✅
	Age of the user
	generalHealth
	String
	

	General health status
	

🔹Nested Type: SinglemedicalUserResponse
Field
	Type
	Required
	Description
	id
	Int
	✅
	Internal record ID
	medicalUserId
	Int
	

	Medical user identifier
	sectionId
	Int
	

	Section reference
	questionId
	Int
	

	Question ID
	questionResponse
	QuestionResponse
	✅
	Question & Answer object
	updatedAt
	String
	

	Last updated timestamp
	

 API: getMyMedicalPoa
Returns the user's Medical Power of Attorney (POA) contact list.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique ID of the user
	

🔸 Response Payload
Field
	Type
	Required
	Description
	message
	String
	✅
	Result message
	success
	Boolean
	✅
	Status of operation
	code
	Int
	✅
	Status code
	error
	String
	

	Error message, if any
	data
	[MymedicalPoaResponseData]
	✅
	List of POA records
	🔹Nested Type: MymedicalPoaResponseData
Field
	Type
	Required
	Description
	id
	Int
	✅
	Record ID
	name
	String
	✅
	Contact name
	contact
	String
	

	Phone number
	email
	String
	

	Email address
	streetName
	String
	

	Street name
	apartmentNameAndNum
	String
	

	Apartment name and number
	apartmentUnitNumber
	String
	

	Unit number
	city
	String
	

	City
	state
	String
	

	State name
	pincode
	String
	

	Postal code
	country
	String
	

	Country name
	contatctType
	String
	

	Type of contact
	contactTypeId
	[Int]
	✅
	List of contact type IDs
	createdAt
	String
	✅
	Created timestamp
	

 API: getHealthAccByUserId
Returns a list of health account credentials saved by a user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Success flag
	message
	String
	✅
	Status message
	error
	String
	

	Error details if any
	data
	[HealthAccountInfo!]
	✅
	List of health accounts
	

🔹Nested Type: HealthAccountInfo
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier
	serviceProvider
	String
	

	Health service provider name
	emailOrUserName
	String
	

	Username or email
	password
	String
	

	Stored password
	note
	String
	

	Notes
	userId
	String
	

	User ID
	createdBy
	String
	

	Created by
	recordIdentifier
	String
	✅
	Unique record reference
	files
	[NotesFiles!]
	

	Attached document files
	createdAt
	String
	

	Creation timestamp
	

🔹Nested Type: NotesFiles
Field
	Type
	Required
	Description
	id
	Int
	

	File identifier
	documentLink
	String
	

	URL to download/view the document
	originalFileName
	String
	

	Original name of the uploaded file
	updatedAt
	String
	

	Last update time
	

 API: getHealthAccById
Returns a specific health account by its ID.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	✅
	User identifier
	ID
	Int
	✅
	Health account ID
	🔸 Response Payload Same structure as HealthAccountInfo.
 API: getSupplements
Fetches all supplement records for a given user.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	GetSupplementInput
	✅
	Supplement filter criteria
	🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation status
	message
	String
	✅
	Status message
	supplements
	[Supplement!]
	✅
	List of supplements
	error
	String
	

	Error message
	

🔹Nested Type: Supplement


Field
	Type
	Required
	Description
	id
	Int
	

	ID of the supplement record
	supplementId
	Int
	✅
	Supplement identifier
	userId
	String
	✅
	User identifier
	supplementName
	String
	✅
	Name of the supplement
	dosage
	String
	✅
	Dosage information
	notes
	String
	✅
	Notes on usage
	important
	Boolean
	✅
	Importance flag
	files
	[supplementFile!]
	✅
	Related files
	createdAt
	String
	✅
	Creation date
	updatedAt
	String
	✅
	Last updated date
	recordIdentifier
	String
	✅
	Unique record ID
	createdBy
	String
	✅
	Record created by
	updatedBy
	String
	✅
	Record last updated by
	

🔹Nested Type: supplementFile


Field
	Type
	Required
	Description
	id
	Int
	✅
	File identifier
	fileContent
	String
	✅
	File content or link
	originalFilename
	String
	✅
	Original file name
	createdAt
	String
	

	File creation timestamp
	createdBy
	String
	✅
	Who created this file
	updatedBy
	String
	✅
	Who last updated this file
	updatedAt
	String
	✅
	Last update timestamp
	API: getSupplementsByID
 Returns a specific supplement based on the filter.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	GetSupplementInput
	            ✅
	Supplement filter criteria
	🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation success
	message
	String
	            ✅
	Response message
	supplement
	Supplement
	

	Specific supplement detail
	error
	String
	

	Error message
	

 API: GetAllHealthVaultFiles
 Returns all the files stored in the user's health vault.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	             ✅
	User identifier
	🔸 Response Payload
Field
	Type
	Required
	Description
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation success
	message
	String
	

	Status message
	error
	String
	

	Error message
	data
	[HealthVaultModules!]
	✅
	Health module file records
	

🔹Nested Type: HealthVaultModules


Field
	Type
	Required
	Description
	subModule
	String
	✅
	Name of the health submodule
	files
	[HealthVaultFiles!]
	✅
	Files stored in the module
	notes
	String
	✅
	Additional notes
	

🔹Nested Type: HealthVaultFiles


Field
	Type
	Required
	Description
	id
	Int
	✅
	File identifier
	originalFileName
	String
	✅
	Name of the uploaded file
	recordId
	Int
	✅
	Related record ID
	

 API: getMedicalageBloodgroupSingle
Returns the user's age and blood group information.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	              ✅
	User identifier
	🔸 Response Payload
Field
	Type
	Required
	Description
	age
	Int
	

	User's age
	bloodGroupId
	Int
	

	ID of the blood group
	bloodGroup
	String
	

	Blood group name
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Request status
	message
	String
	

	Additional info message
	error
	String
	

	Error message
	

 API: emergencyAlert
 Returns emergency alert conditions related to the user.
🔸 Request Payload
Field
	Type
	Required
	Description
	userId
	String
	                ✅
	User identifier
	🔸 Response Payload
Field
	Type
	Required
	Description
	datas
	[emergencyAlertData!]
	✅
	Emergency data records
	code
	Int
	✅
	Status code
	success
	Boolean
	✅
	Operation result
	message
	String
	

	Status message
	error
	String
	

	Error message
	

🔹Nested Type: emergencyAlertData


Field
	Type
	Required
	Description
	diseaseName
	String
	

	Name of the disease
	diseaseDescription
	String
	

	Description of the disease
	diseaseFile
	String
	

	File path or content
	diseaseFileName
	String
	

	Name of the attached file
	emergencyAlert
	String
	

	Alert type
	rId
	Int
	

	Record ID
	fileId
	Int
	

	Associated file ID
	relationship
	String
	

	Relationship of the user
	

 API: braceletAhd
Returns all AHD (Advanced Health Directive) contacts.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	ListAllAhdContactsInput
	

	Filtering input if any
	🔸 Response Payload
Field
	Type
	Required
	Description
	ahd
	[ahd]
	                  ✅
	List of AHD contact records
	 API: getHealthVaultFiles
Returns a specific file stored in the user's health vault by input filters.
🔸 Request Payload
Field
	Type
	Required
	Description
	input
	GetHealthVaultFilesInput
	                  ✅
	Input containing file ID or filters.
	🔸 Response Payload
Field
	Type
	Required
	Description
	name
	String
	✅
	Name of the document
	fileID
	Int
	✅
	File identifier
	subModule
	String
	✅
	Name of the sub-module
	fileContent
	String
	✅
	Raw content of the file
	API: getAgentWitnessDetails
Returns agent or witness details based on the given ID and type.
🔸 Request Payload
Field
	Type
	Required
	Description
	id
	Int
	✅
	Record identifier
	type
	String
	✅
	"agent" or "witness"
	🔸 Response Payload
Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier
	email
	String
	✅
	Email address
	mobile
	String
	✅
	Contact mobile number
	modules
	String
	✅
	Modules this record is linked to
	customerName
	String
	✅
	Name of the customer
	name
	String
	✅
	Name of agent or witness
	sharedContent
	String
	✅
	Shared notes/content
	message
	String
	✅
	Status message
	success
	Boolean
	✅
	Indicates if request succeeded
	code
	Int
	✅
	Status code
	error
	String
	

	Error message if any
	startDate
	String
	

	Start date for agent/witness role
	





________________






API: CreateNotification
Creates a new notification entry in the system for the recipient user.
🔸 Request Payload


Field
	Type
	R/O
	Description
	id
	Int
	

	Unique identifier of the notification (auto-generated)
	recordId
	[Int!]
	✅
	Array of related record IDs associated with the notification
	senderUserId
	String
	

	UUID of the user sending the notification
	senderUserName
	String
	

	Name of the sender
	recipientUserId
	String
	

	UUID of the user receiving the notification
	recipientUserName
	String
	

	Name of the recipient
	title
	String
	

	Title or subject of the notification
	sendersContent
	String
	

	Message content displayed to the sender
	recipientContent
	String
	

	Message content displayed to the recipient
	link
	String
	

	Optional URL associated with the notification
	notificationType
	String
	

	Type of notification (serviceName in request is mapped here)
	sharedModules
	[String!]
	✅
	Modules being shared with the recipient
	psType
	Int
	

	Type of Power of Attorney (e.g., General, Medical, etc.)
	sharedVaults
	[String!]
	✅
	Vaults being shared
	serviceName
	String
	

	Name of the originating service or module
	isButtonEnabled
	Boolean
	

	Enables a button (e.g., to take action) in the UI
	isAccessButtonEnabled
	Boolean
	

	Enables an additional access button in the UI
	createDate
	String
	

	Timestamp when the notification was created
	createdBy
	String
	

	UUID of the user who created the notification
	



🔸 Response Fields


Field
	Type
	R/O
	Description
	success
	Boolean
	✅
	true if notification was successfully created.
	message
	String
	✅
	Description of the operation outcome.
	code
	Int
	✅
	HTTP-like status code (e.g., 200, 400).
	errorMessage
	String
	✅
	Error message, if any.
	



API: ReadNotification


🔸 Request Payload


Field
	Type
	R/O
	Description
	userId
	String
	✅
	ID of the user who is reading the notification.
	id
	Int
	✅
	ID of the notification to mark as read.
	

🔸 Response Fields


Field
	Type
	R/O
	Description
	code
	Int
	✅
	Status code.
	success
	Boolean
	✅
	true if the operation was successful.
	message
	String
	✅
	Outcome message.
	error
	String
	

	Error message if any.


	



	

	API: UpdateNotification


🔸 Request Payload


Field
	Type
	R/O
	Description
	Id
	Int
	✅
	Notification ID.
	userId
	String
	✅
	User updating the approval status.
	Approvestatus
	Int
	✅
	New approval status value.
	

🔸 Response Fields


Field
	Type
	R/O
	Description
	code
	Int
	✅
	Status code.
	success
	Boolean
	✅
	true if the operation was successful.
	message
	String
	✅
	Outcome message.
	error
	String
	

	Error message if any.


	



	

	API: NotificationStream


🔸 Request Payload


Field
	Type
	R/O
	Description
	userId
	String
	✅
	ID of the user to stream notifications for.
	filter
	String
	✅
	Optional filter for notification types.
	

🔸 Response Fields


Field
	Type
	R/O
	Description
	code
	Int
	✅
	Status code.
	success
	Boolean
	✅
	Indicates success of the operation.
	message
	String
	✅
	Response message.
	error
	String
	

	Error message if any.
	unreadCount
	Int
	✅
	Total unread notifications.
	sentUnreadCount
	Int
	✅
	Total unread sent notifications.
	recieveUnreadCount
	Int
	✅
	Total unread received notifications.
	data
	[NotificationData!]
	✅
	List of notifications.
	



🔹 Nested Type: NotificationData




Field
	Type
	

	M/O
	Description
	id
	Int
	

	✅
	Notification ID.
	title
	String
	

	✅
	Notification title.
	description
	String
	

	✅
	Description or content of the notification.
	link
	String
	

	✅
	Link associated with the notification.
	createDate
	String
	

	✅
	Creation date (ISO format).
	modelName
	String
	

	✅
	Related model/entity name.
	isReadBySender
	Boolean
	

	✅
	Has the sender read the notification.
	isReadByRecipient
	Boolean
	

	✅
	Has the recipient read the notification.
	isButtonEnabled
	Boolean
	

	✅
	Whether buttons (like approve) are active.
	senderUserId
	String
	

	✅
	ID of the sender.
	senderUserName
	String
	

	✅
	Name of the sender.
	recipientUserId
	String
	

	

	ID of the recipient.
	recipientUserName
	String
	

	

	Name of the recipient.
	recordId
	[Int!]
	

	✅
	Associated record identifiers.
	sharedModules
	[String!]
	

	✅
	Names of shared modules.
	approvedStatus
	String
	

	

	Approval status.
	notifiactionType
	String
	

	✅
	Type/category of notification.
	recieverType
	String
	

	

	Type/category of recipient (e.g., user/admin).
	isAccessButtonEnabled
	Boolean
	

	

	Whether access-related button is enabled.
	psType
	Int
	

	✅
	Persona/service type.
	vaults
	[String!]
	

	✅
	Shared vault identifiers.
	personaId
	String
	

	✅
	Persona identifier.
	sharedModuleIds
	[Int!]
	

	✅
	IDs of shared modules.
	poaOrWitnessId
	Int
	

	

	ID of associated POA or Witness (if applicable).
	







API List - Subscription - Query 


 Api: listSubscriptions 
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier of the user.
	

🔸Response Fields


Field
	Type
	Required
	Description
	UserID
	String
	✅
	The user ID for which subscriptions were fetched.
	Success
	String
	✅
	Whether the operation was successful.
	Code
	String
	✅
	Status code from the microservice.
	Message
	String
	✅
	Any message from the microservice.
	ErrorMessage
	String
	✅
	Any error message from the microservice.
	SubscriptionHistory
	[Subscriptions]
	✅
	The list of all past subscriptions
	ActivePlan
	Subscriptions
	✅
	The currently active subscription plan, if any.
	

🔸Nested Type: Subscriptions


Field
	Type
	Required
	Description
	UserID
	String
	✅
	The ID of the user who owns the subscription.
	PlanID
	int
	✅
	The ID of the subscription plan
	Plan
	String
	✅
	The name of the subscription plan.
	TenureID
	String
	✅
	The ID represents the tenure (duration) of the subscription.
	Tenure
	String
	✅
	The name or description of the tenure.
	StartDate
	String
	✅
	The date when the subscription started.
	ExpiryOn
	String
	✅
	The date when the subscription will expire.
	AmountBeforeDiscount
	float64
	✅
	The original amount before any discounts were applied.
	TotalDiscount
	float64
	✅
	The total discount applied to the subscription.
	AmountPaid
	float64
	✅
	The final amount paid after discounts.
	TransactionTime
	String
	✅
	The time when the transaction occurred.
	AutoRenew
	bool
	✅
	Indicates if the subscription is set to auto-renew.
	TransactionID
	String
	✅
	The ID of the transaction for the subscription.
	StripeCustomerID
	String
	✅
	The Stripe customer ID associated with the subscription.
	CreatedBy
	String
	✅
	The user or system that created the subscription record.
	UpdatedBy
	String
	✅
	The user or system that last updated the subscription record.
	CreatedAt
	String
	✅
	The timestamp when the subscription record was created
	UpdatedAt
	String
	✅
	The timestamp when the subscription record was last updated.
	ID
	Int
	✅
	The unique ID of the subscription record
	IsActive
	bool
	✅
	Indicates if the subscription is currently active.
	

 API: getPricingPlans 
🔸 Request Payload
Nothing


🔸Response Fields


Field
	Type
	Required
	Description
	Message
	string
	✅
	Informational message about the request.
	Success
	bool
	✅
	Indicates if the request was successful.
	Code
	int
	✅
	Status code for the response.
	Error
	string
	✅
	Error message, if any.
	PricingPlans
	[PricingPlans]
	✅
	List of all pricing plans.
	

🔸Nested Type: PricingPlans


Field
	Type
	Required
	Description
	ID
	int
	✅
	Unique identifier for the plan.
	PlanName
	string
	✅
	Name of the pricing plan.
	PlanDescription
	string
	✅
	Description of the plan
	MonthlyPrice
	float64
	✅
	Price for monthly subscription
	YearlyPrice
	float64
	✅
	Price for yearly subscription
	MonthlyPriceID
	string
	✅
	Identifier for monthly price
	YearlyPriceID
	string
	✅
	Identifier for yearly price.
	ThreeYearPriceID
	string
	✅
	Identifier for three-year price.
	LifetimePriceID
	string
	✅
	Identifier for lifetime price.
	PlanFeatures
	[string]
	✅
	List of features included in the plan.
	

API :- getTenure
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier of the user.
	

🔸Response Fields


Field
	Type
	Required
	Description
	Code
	int
	✅
	Status code for the response
	Success
	bool
	✅
	Indicates if the request was successful
	Message
	string
	✅
	Informational message about the request
	Tenure
	[Tenure]
	✅
	List of available tenures
	Error
	string
	

	Error message, if any
	

🔸Nested Type: Tenure


Field
	Type
	Required
	Description
	ID
	int
	✅
	Unique identifier for the tenure.
	TenureYears
	String
	✅
	Duration of the tenure.
	

API:- getPlanFeatures
🔸 Request Payload
Nothing


🔸Response Fields


Field
	Type
	Required
	Description
	pricingTable
	[PricingTable]
	✅
	List of pricing tables (vaults and modules)
	code
	Int!
	✅
	Status code
	success
	Boolean
	✅
	Indicates if the request was successful
	message
	String
	

	Informational message
	error
	String
	

	Error message, if any
	

🔸Nested Type: PricingTable


Field
	Type
	Required
	Description
	vaults
	[Vault]
	✅
	List of vaults with modules
	

🔸Nested Type: Vault


Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier for the vault
	title
	String
	✅
	Name/title of the vault
	modules
	[Module]
	✅
	List of modules in the vault
	

🔸Nested Type: Module


Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier for the module
	title
	String
	✅
	Name/title of the module
	priced
	Boolean
	✅
	Indicates if the module is priced
	basic
	Boolean
	✅
	Availability in Basic plan
	standard
	Boolean
	✅
	Availability in Standard plan
	advanced
	Boolean
	✅
	Availability in Advanced plan
	subModules
	[SubModule]
	✅
	List of submodules
	

🔸Nested Type: SubModule


Field
	Type
	Required
	Description
	title
	String
	✅
	Title of the submodule
	basic
	Boolean
	✅
	Availability in Basic plan
	standard
	Boolean
	✅
	Availability in Standard plan
	advanced
	Boolean
	✅
	Availability in Advanced plan
	

API:- getPriceComparison
🔸 Request Payload
Nothing


🔸Response Fields


Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates if the request was successful.
	message
	String
	✅
	Informational message about the request.
	code
	Int
	✅
	Status or response code.
	plans
	[PriceComparison]
	✅
	List of plan comparisons (see below for nested structure).
	

🔸Nested Type: PriceComparison


Field
	Type
	Required
	Description
	planId
	Int
	✅
	Unique identifier for the plan.
	planName
	String
	✅
	Name of the subscription plan.
	planDescription
	String
	✅
	Description of the subscription plan.
	typesOfPlan
	[PlanDuration]
	✅
	List of available durations and their pricing (see below).
	

🔸Nested Type: PlanDuration


Field
	Type
	Required
	Description
	duration
	String
	✅
	Duration label (e.g., "Monthly", "Yearly").
	price
	Int
	✅
	Price for the specified duration.
	discount
	String
	

	Discount information, if any.
	

API: listCoupons
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	Unique identifier of the user.
	

🔸Response Fields


Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates if the request was successful.
	message
	String
	✅
	Informational message about the request.
	code
	Int
	✅
	Status or response code.
	data
	[Coupon]
	✅
	List of coupon objects (see below for nested structure).
	

🔸Nested Type: Coupon


Field
	Type
	Required
	Description
	id
	Int
	✅
	Unique identifier for the coupon.
	code
	String
	✅
	Coupon code.
	type
	String
	✅
	Type of coupon (e.g., percentage, flat).
	discount
	Int
	✅
	Discount value.
	maxDiscount
	Int
	✅
	Maximum discount allowed.
	startDate
	String
	✅
	Start date of coupon validity.
	expiryDate
	String
	✅
	Expiry date of coupon validity.
	userId
	String
	

	User ID associated with the coupon (if applicable).
	eventName
	String
	

	Event name associated with the coupon.
	usageLimit
	Int
	✅
	Maximum number of times the coupon can be used.
	usedCount
	Int
	✅
	Number of times the coupon has been used.
	description
	String
	

	Description of the coupon.
	 
API: discountAmount
🔸 Request Payload


Field
	Type
	Required
	Description
	planId
	int
	✅
	The unique identifier of the subscription plan
	tenureId
	int
	✅
	The unique identifier of the tenure/duration
	

🔸Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Informational message about the request.
	success
	Boolean
	✅
	Indicates if the request was successful.
	code
	Int
	✅
	Status or response code.
	error
	String
	✅
	Error message if the request fails.
	amount
	Float
	✅
	Original amount before discount.
	amountAfterDiscount
	Float
	✅
	Final amount after applying the discount.
	discountMessage
	String
	

	Message describing the discount applied, if any.
	

 API: getPlan 
🔸 Request Payload


Field
	Type
	Required
	Description
	planId
	int
	

	The unique identifier of the subscription plan.
	subModuleId
	int
	

	The unique identifier of the submodule.
	

🔸Response Fields


Field
	Type
	Required
	Description
	status
	bool
	

	Indicates the status or existence of the plan or submodule
	



API: getSubscriptionInvoice
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	

	The unique identifier of the user.
	subscriptionId
	int
	

	The unique identifier of the subscription.
	

🔸Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Informational message about the request.
	success
	Boolean
	✅
	Indicates if the request was successful.
	code
	Int
	✅
	Status or response code.
	error
	String
	

	Error message if the request fails.
	invoiceNumber
	String
	✅
	Unique invoice number.
	invoiceDate
	String
	✅
	Date of the invoice.
	subscriptionPlanName
	String
	✅
	Name of the subscription plan.
	subscriptionPlanType
	String
	✅
	Type of the subscription plan.
	subscriptionStartDate
	String
	✅
	Start date of the subscription.
	subscriptionExpiryDate
	String
	✅
	Expiry date of the subscription.
	autoRenew
	Boolean
	✅
	Whether the subscription is set to auto-renew.
	subscriptionFee
	Float
	✅
	Subscription fee amount.
	tax
	Float
	✅
	Tax amount applied.
	discount
	Float
	✅
	Discount amount applied.
	totalAmount
	Float
	✅
	Total amount to be paid.
	paymentMethod
	String
	✅
	Payment method used.
	Name
	String
	✅
	Name of the user.
	email
	String
	✅
	Email address of the user.
	Address
	String
	✅
	Billing address of the user.
	

API List - Mutation


 API: cancelSubscription
🔸 Request Payload


Field
	Type
	Required
	Description
	id
	Int
	✅
	The unique identifier of the subscription to cancel.
	userId
	String
	✅
	The unique identifier of the user.
	updatedBy
	String
	✅
	The identifier of the user performing the cancellation.
	

🔸Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Informational message about the request.
	success
	Boolean
	✅
	Indicates if the request was successful.
	code
	Int
	✅
	Status or response code.
	error
	String
	

	Error message if the request fails.
	

 API: proceedToCheckOut
🔸 Request Payload


Field
	Type
	Required
	Description
	userId
	String
	✅
	The unique identifier of the user.
	planId
	Int
	✅
	The unique identifier of the subscription plan.
	tenureId
	Int
	✅
	The unique identifier of the tenure/duration.
	priceId
	String
	✅
	The price identifier (e.g., Stripe price ID).
	couponId
	Int
	✅
	The unique identifier of the coupon to apply.
	

🔸Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Informational message about the request.
	success
	Boolean
	✅
	Indicates if the request was successful.
	code
	Int
	✅
	Status or response code.
	error
	String
	

	Error message if the request fails.
	sessionId
	String
	✅
	Session ID for payment processing.
	

 API: addCoupon
🔸 Request Payload


Field
	Type
	Required
	Description
	code
	String
	✅
	The coupon code.
	type
	String
	✅
	The type of coupon (e.g., percentage, flat).
	discount
	Float
	✅
	The discount value.
	maxDiscount
	Float
	

	The maximum discount allowed.
	startDate
	String
	✅
	The start date of coupon validity.
	expiryDate
	String
	✅
	The expiry date of coupon validity.
	eventName
	String
	

	The event name associated with the coupon.
	usageLimit
	Int
	

	The maximum number of times the coupon can be used.
	couponDescription
	String
	

	Description of the coupon.
	

🔸Response Fields


Field
	Type
	Required
	Description
	message
	String
	✅
	Informational message about the request.
	couponId
	Int
	✅
	Unique identifier of the newly added coupon.
	code
	Int
	✅
	Status or response code.
	success
	Boolean
	✅
	Indicates if the request was successful.
	

 API: applyCoupon
🔸 Request Payload


Field
	Type
	Required
	Description
	code
	String
	✅
	The coupon code to apply.
	userId
	String
	✅
	The unique identifier of the user.
	orderAmount
	Float
	✅
	The total order amount before discount.
	

🔸Response Fields


Field
	Type
	Required
	Description
	errorMessage
	String
	

	Error message if the request fails.
	success
	Boolean
	✅
	Indicates if the request was successful.
	message
	String
	✅
	Informational message about the request.
	couponCode
	String
	

	The applied coupon code.
	appliedDiscount
	Float
	

	The discount amount applied.
	code
	Int
	✅
	Status or response code.
	planId
	Int
	

	The plan ID associated with the coupon.